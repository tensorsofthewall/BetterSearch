import importlib
import numpy as np
import numpy.typing as npt
from chromadb.api.types import EmbeddingFunction, Documents, Embeddings, Document
from typing import Optional, List

class EmbeddingModelFunction(EmbeddingFunction[Documents]):
    def __init__(self, model_name: str = "Alibaba-NLP/gte-base-en-v1.5", cache_dir: Optional[str] = None):
        try:
            from transformers import AutoModel, AutoTokenizer
            self._torch = importlib.import_module("torch")
            self._model = AutoModel.from_pretrained(model_name, cache_dir=cache_dir, trust_remote_code=True)
            self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        except ImportError:
            raise ValueError("The sentence-transformers package is not installed. Please install it with "
            "'pip install sentence-transformers'")
        
    @staticmethod
    def _normalize(vector: npt.NDArray) -> npt.NDArray:
        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector
        return vector / norm
    
    def __call__(self, input: List[Document]) -> Embeddings:
        inputs = self._tokenizer(input, padding=True, truncation=True, return_tensors="pt")
        
        with self._torch.no_grad():
            outputs = self._model(**inputs)
        
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return [e.tolist() for e in self._normalize(embeddings)]