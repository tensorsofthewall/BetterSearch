from .file_indexer  import WindowsFileIndexer, LinuxFileIndexer
from .pipeline import BetterSearchPipeline


APP_NAME="BetterSearch"
VERSION="0.1.0"

__SUPPORTED_MODELS__ = [
    "sandeshb/llama-3-sqlcoder-8b-int8-ov",
    "defog/llama-3-sqlcoder-8b"
]