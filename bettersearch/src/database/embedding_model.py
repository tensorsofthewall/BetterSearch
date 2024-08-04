import numpy as np
import numpy.typing as npt
from chromadb.api.types import EmbeddingFunction, Documents, Embeddings, Document
from typing import Optional, List
import logging
import torch

logger = logging.getLogger(__name__)

class EmbeddingModelFunction(EmbeddingFunction[Documents]):
    def __init__(self, model_name: str = "Alibaba-NLP/gte-base-en-v1.5", cache_dir: Optional[str] = None, device: str = "cpu"):
        """
        Initialize the EmbeddingModelFunction with the given parameters.

        Args:
            model_name (str): Name of the pre-trained model to use.
            cache_dir (Optional[str]): Directory to cache the model.
            device (str): Device to run the model on (e.g., "cpu", "cuda").
        """
        try:
            from transformers import AutoModel, AutoTokenizer
            self._device = torch.device(device)
            self._model = AutoModel.from_pretrained(
                pretrained_model_name_or_path=model_name, 
                cache_dir=cache_dir, 
                trust_remote_code=True,
                unpad_inputs=True, 
                use_memory_efficient_attention=True if self._device == "cuda" else False, #xformers-enable (do not enable on Windows, attn_bias device issue)
            ).to(self._device)
            
            self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        except ImportError:
            logger.error("The transformers package is not installed. Please install it with "
            "'pip install transformers'")
        
    @staticmethod
    def _normalize(vector: npt.NDArray) -> npt.NDArray:
        """
        Normalize the given vector to unit length.

        Args:
            vector (npt.NDArray): Input vector to be normalized.

        Returns:
            npt.NDArray: Normalized vector.
        """
        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector
        return vector / norm
    
    def __call__(self, input: List[Document]) -> Embeddings:
        """
        Generate embeddings for the given input documents.

        Args:
            input (List[Document]): List of documents to generate embeddings for.

        Returns:
            Embeddings: List of embeddings for the input documents.
        """
        # Tokenize the input documents
        inputs = self._tokenizer(input, padding=True, truncation=True, return_tensors="pt").to(self._device)
        
        # Generate embeddings using the model
        with torch.autocast(device_type=self._device.type, dtype=torch.float16):
            with torch.inference_mode():
                outputs = self._model(**inputs)
        
        embeddings = outputs.last_hidden_state.mean(dim=1)
        if self._device.type == "cpu":
            embeddings = embeddings.cpu()
            
        # Normalize and return the embeddings
        return [e.tolist() for e in self._normalize(embeddings)]