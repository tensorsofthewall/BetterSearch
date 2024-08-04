from setuptools import setup, find_packages

VERSION = '0.1.0'
DESCRIPTION = "An improved file search system that draws inspiration from traditional Search and combines with vector databases, allowing local LLMs to search files as context for answering user queries."

setup(
    name="bettersearch",
    version=VERSION,
    author="Sandesh Bharadwaj",
    author_email="sandesh.bharadwaj97@gmail.com",
    description=DESCRIPTION,
    install_requires=[
        "python-ffmpeg",
        "pillow",
        "pymupdf4llm"    
    ],
    url="https://github.com/sandesh-bharadwaj/BetterSearch",
)