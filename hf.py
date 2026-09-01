from huggingface_hub import snapshot_download
from dotenv import load_dotenv
import argparse

load_dotenv()

def download_model(name: str, repo_type: str, outpath: str = None, allow_patterns: list = None) -> None:
    snapshot_download(
        repo_id=name, 
        local_dir=outpath or f"./{name}",
        repo_type=repo_type,
        allow_patterns=allow_patterns
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download resources from Hugging Face Hub.")
    parser.add_argument("--name", type=str, required=True, help="The name of the model/dataset/space.")
    parser.add_argument("--type", type=str, choices=["model", "dataset", "space"], default="model", help="The type of resource.")
    parser.add_argument("--outpath", type=str, help="The output path.")
    
    # nargs='*' allows you to pass multiple patterns separated by spaces
    parser.add_argument("--allow-patterns", nargs="*", help="One or more file patterns to match, e.g. '*.gguf' '*.json'")
    args = parser.parse_args()
    
    print(f"Downloading {args.type} '{args.name}' to {args.outpath or f'./{args.name}'} with patterns {args.allow_patterns or 'all'}...")
    
    download_model(args.name, args.type, args.outpath, args.allow_patterns)