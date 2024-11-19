# System libraries
import logging
from pathlib import Path
from operator import itemgetter

# Installed libraries
from tqdm import tqdm
from langchain_text_splitters import MarkdownTextSplitter, RecursiveCharacterTextSplitter
import chromadb

# Others
from .constants import parsable_exts
from .parse import parse_file_contents
from .util import flatten
from .embedding_model import EmbeddingModelFunction
from bettersearch.database.base_db_handler import BaseDBHandler  # Import the base interface

logger = logging.getLogger(__name__)

class ChromaDBHandler(BaseDBHandler):
    def __init__(self, 
                 vector_db_path: str = "better_search_content_db", 
                 embedding_model_name: str = "Alibaba-NLP/gte-base-en-v1.5", 
                 chunk_size: int = 500, chunk_overlap: int = 200, top_k: int = 5, 
                 chunk_batch_size: int = 500, cache_dir: str = None, device: str = "cpu",
                 **kwargs
                 ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model_name = embedding_model_name
        self.cache_dir = cache_dir
        self.embedding_model_fn = EmbeddingModelFunction(
            model_name=self.embedding_model_name,
            cache_dir=self.cache_dir,
            device=device
        )
        
        self.db = chromadb.PersistentClient(
            path=vector_db_path, 
            settings=chromadb.config.Settings(),   
        )
        
        self.collection = self.db.get_or_create_collection(
            name="file-content",
            embedding_function=self.embedding_model_fn,
        )
        
        self._top_k = top_k
        self.batch_size = chunk_batch_size
    
    @property
    def top_k(self):
        return self._top_k    
    
    @top_k.setter
    def top_k(self, value):
        self._top_k = value
        
    def _create_docs_for_db(self, file_path=None, date_modified=None):
        content = parse_file_contents(file_path)
        ext = Path(file_path).suffix
        if isinstance(content, str):
            if ext in parsable_exts.get("mupdf"):
                splitter = MarkdownTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
            elif ext in parsable_exts.get("text"):
                splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
            
            docs = [doc.page_content for doc in splitter.create_documents([content])]
            metadatas = [{"path": f"{file_path}", "fileext": f"{ext}", "date_modified": str(date_modified)} for _ in range(len(docs))]
            ids = [f"{file_path}_{i+1}" for i in range(len(docs))]
            return {"documents": docs, "metadatas": metadatas, "ids": ids}, len(docs)
        else:
            return None, None
    
    def add_to_collection(self, file_path=None, date_modified=None):
        try:
            data, num_docs = self._create_docs_for_db(file_path=file_path, date_modified=date_modified)
            if num_docs:
                for i in range(0, num_docs, self.batch_size):
                    self.collection.add(
                        documents=data.get("documents")[i:i+self.batch_size],
                        metadatas=data.get("metadatas")[i:i+self.batch_size],
                        ids=data.get("ids")[i:i+self.batch_size],
                    )
        except Exception as e:
            logger.error(f"File failed: {file_path}")
            logger.exception(e)
    
    def update_to_collection(self, file_path=None, date_modified=None):
        try:
            data, num_docs = self._create_docs_for_db(file_path=file_path, date_modified=date_modified)
            if num_docs:
                for i in range(0, num_docs, self.batch_size):
                    self.collection.update(
                        documents=data.get("documents")[i:i+self.batch_size],
                        metadatas=data.get("metadatas")[i:i+self.batch_size],
                        ids=data.get("ids")[i:i+self.batch_size],
                    )
        except Exception as e:
            logger.error(f"File failed: {file_path}")
            logger.exception(e)
    
    def delete_from_collection(self, file_path=None):
        self.collection.delete(where={"path": file_path})
    
    def update_collection(self, change_list):
        for change in tqdm(change_list):
            change_type, file_path, date_modified = itemgetter("ChangeType", "path", "date_modified")(change)
            if change_type == 'Deleted':
                self.delete_from_collection(file_path=file_path)
            elif change_type == 'Added':
                self.add_to_collection(file_path=file_path, date_modified=date_modified)
            elif change_type == 'Modified':
                self.update_to_collection(file_path=file_path, date_modified=date_modified)
    
    def query_collection(self, query):
        docs = self.collection.query(query_texts=[query], n_results=self.top_k).get('documents')[0]
        return "\n\n".join(str(x) for x in flatten(docs))
