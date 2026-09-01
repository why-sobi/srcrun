from huggingface_hub import snapshot_download
from dotenv import load_dotenv
import argparse

load_dotenv()

def download_model(name: str, repo_type: str) -> None:
    """
    Download a model/dataset/space from Hugging Face Hub.

    Args:
        name (str): The name of the model/dataset/space to download.
        repo_type (str): The type of the resource to download.
    """
    snapshot_download(
        repo_id=name, 
        local_dir=f"./{name}",
        repo_type=repo_type
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download a model/dataset/space from Hugging Face Hub.")
    parser.add_argument("--name", type=str, help="The name of the model/dataset/space to download.")
    parser.add_argument("--type", type=str, choices=["model", "dataset", "space"], default="model", help="The type of the resource to download (default: model).")
    args = parser.parse_args()
    
    download_model(args.name, args.type)