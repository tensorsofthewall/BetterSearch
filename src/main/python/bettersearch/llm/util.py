import os
from huggingface_hub import snapshot_download

def download_hf_model_with_naming(repo_id, base_dir):
    """
    THIS IS A WIP, DO NOT USE UNTIL FURTHER NOTICE.
    For this to work, need to replicate the HF Cache structure i.e. models--model_name/refs,blobs,snapshots and all that. Transformers redownloads the models currently even if they're present in base_dir.
    
    Downloads a Hugging Face model repository to a custom directory with the naming convention
    'models--model_name' (similar to Hugging Face's transformers library).

    Args:
        repo_id (str): The repository ID of the model on Hugging Face Hub (e.g., "bert-base-uncased").
        base_dir (str): The base directory where the model-specific folder will be created.

    Returns:
        str: The path to the downloaded model directory.
    """
    os.environ['HF_HUB_ENABLE_HF_TRANSFER'] = "1"
    # Create a directory name following the Hugging Face style: models--model_name
    safe_repo_id = repo_id.replace("/", "--")  # Replace "/" with "--" for compatibility
    model_dir_name = f"models--{safe_repo_id}"
    target_dir = os.path.join(base_dir, model_dir_name)

    # Ensure the base directory exists
    os.makedirs(base_dir, exist_ok=True)

    # Download the repository snapshot to the target directory
    model_path = snapshot_download(
        repo_id=repo_id,
        repo_type="model", 
        local_dir=target_dir, 
        local_dir_use_symlinks=False,
        ignore_patterns=["*.md"]
    )
    
    return model_path