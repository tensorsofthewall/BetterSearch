from setuptools import setup

VERSION = '0.0.1'
DESCRIPTION = "An improved file search system that draws inspiration from Windows Search and indexes both file properties and file content, allowing local LLMs to search and use this data as context for answering user queries."


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
)