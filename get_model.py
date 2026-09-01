from huggingface_hub import snapshot_download
from dotenv import load_dotenv
import argparse

load_dotenv()

def download_model(name: str) -> None:
    """
    Download a model from Hugging Face Hub.

    Args:
        name (str): The name of the model to download.
    """
    snapshot_download(
        repo_id=name, 
        local_dir=f"./{name}",
        repo_type="model"
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download a model from Hugging Face Hub.")
    parser.add_argument("name", type=str, help="The name of the model to download.")
    args = parser.parse_args()
    
    download_model(args.name)