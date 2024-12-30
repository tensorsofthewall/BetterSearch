# System libraries
import logging

# Installed libraries
import chromadb
from collections import defaultdict
from typing import Union, List

# Others
from .parse import create_docs_for_db
from .util import flatten
from .embedding_model import EmbeddingModelFunction
from .base_db_handler import BaseDBHandler  # Import the base interface

logger = logging.getLogger(__name__)

class ChromaDBHandler(BaseDBHandler):
    def __init__(self, 
                 vector_db_path: str = "better_search_content_db", 
                 embedding_model_name: str = "Alibaba-NLP/gte-base-en-v1.5", 
                 chunk_size: int = 500, chunk_overlap: int = 200, top_k: int = 5, 
                 chunk_batch_size: int = 500, device: str = "cpu",
                 **kwargs
                 ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model_name = embedding_model_name
        self.cache_dir = kwargs.get("cache_dir", None)
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
            metadata={"hnsw:space": "cosine"}
        )
        
        self._top_k = top_k
        self.batch_size = chunk_batch_size
    
    @property
    def top_k(self):
        return self._top_k    
    
    @top_k.setter
    def top_k(self, value):
        self._top_k = value
    
    def _add_to_collection(self, files):
        for item_dict in files:
            try:
                data, num_docs = create_docs_for_db(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap, file_info=item_dict)
                if num_docs:
                    for i in range(0, num_docs, self.batch_size):
                        self.collection.add(
                            documents=data.get("documents")[i:i+self.batch_size],
                            metadatas=data.get("metadatas")[i:i+self.batch_size],
                            ids=data.get("ids")[i:i+self.batch_size],
                        )
            except Exception as e:
                logger.error(f"File failed: {item_dict.get('path')}")
                logger.exception(e)
    
    def _update_to_collection(self, files):
        for item_dict in files:
            try:
                data, num_docs = create_docs_for_db(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap, file_info=item_dict)
                if num_docs:
                    for i in range(0, num_docs, self.batch_size):
                        self.collection.update(
                            documents=data.get("documents")[i:i+self.batch_size],
                            metadatas=data.get("metadatas")[i:i+self.batch_size],
                            ids=data.get("ids")[i:i+self.batch_size],
                        )
            except Exception as e:
                logger.error(f"File failed: {item_dict.get('path')}")
                logger.exception(e)
    
    def _delete_from_collection(self, file_paths: Union[List[str], str,None]):
        if isinstance(file_paths, str):
            self.collection.delete(where={"path": file_paths})
        elif isinstance(file_paths, list):
            self.collection.delete(where={"path": {"$in": file_paths}})
                
    def get_all_metadata(self):
        db_metadata = self.collection.get(include=["metadatas"]).get("metadatas")
        aggregate_metadata = defaultdict(lambda: {'number_of_chunks': 0})
        if db_metadata:
            for item in db_metadata:
                path = item.pop('path')
                if 'number_of_shards' not in aggregate_metadata[path]:
                    aggregate_metadata[path].update(item)
                aggregate_metadata[path]['number_of_chunks'] += 1
        
        return {"source": "chroma", "data": aggregate_metadata}
    
    def query_collection(self, query, **kwargs):
        if kwargs.get("file_filter"):
            paths = {key: str(val) for key,val in kwargs.get("file_filter") if "path" in key}
            if len(paths.keys()) == 1:
                try:
                    paths = kwargs.get("file_filter")["data"]["path"]
                    metadata_filter = {"path": list(paths.values())}
                except:
                    metadata_filter = None
        else:
            metadata_filter = None
        
        try:
            docs = self.collection.query(query_texts=[query], n_results=self.top_k, where={"metadata_field": metadata_filter} if metadata_filter else None).get('documents')
        except Exception as e:
            docs = []
        return "\n\n".join(str(x) for x in flatten(docs)) if docs else ""
