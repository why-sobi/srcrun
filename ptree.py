import argparse
from pathlib import Path

def print_tree(
    dir_path: Path,
    prefix: str = "",
    exclude_dirs: set = None,
    allowed_exts: set = None
):
    exclude_dirs = exclude_dirs or set()
    allowed_exts = allowed_exts or set()

    items = []
    for path in dir_path.iterdir():
        if path.is_dir():
            if path.name not in exclude_dirs:
                items.append(path)
        elif path.is_file():
            # If no allowed extensions were passed, allow all files; otherwise filter
            if not allowed_exts or path.suffix.lower() in allowed_exts:
                items.append(path)

    items.sort(key=lambda p: (not p.is_dir(), p.name.lower()))

    count = len(items)
    for i, item in enumerate(items):
        is_last = (i == count - 1)
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{item.name}")

        if item.is_dir():
            child_prefix = prefix + ("    " if is_last else "│   ")
            print_tree(
                item,
                prefix=child_prefix,
                exclude_dirs=exclude_dirs,
                allowed_exts=allowed_exts
            )

def main():
    parser = argparse.ArgumentParser(
        description="Print a filtered visual directory tree."
    )
    
    # Optional positional argument for directory path (defaults to current directory)
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        type=Path,
        help="Target directory path (default: current directory)"
    )
    
    # Flag to override excluded directories
    parser.add_argument(
        "-e", "--exclude",
        nargs="*",
        default=["venv", ".git", ".vscode", "__pycache__"],
        help="Directories to exclude from output"
    )
    
    # Flag to override file extensions
    parser.add_argument(
        "-x", "--ext",
        nargs="*",
        default=[".md", ".py", ".hpp", ".cpp"],
        help="File extensions to include (e.g. .py .md). Pass empty to include all files."
    )

    args = parser.parse_args()
    
    # Format user arguments into sets
    exclude_dirs = set(args.exclude)
    allowed_exts = {(ext if ext.startswith('.') else f'.{ext}').lower() for ext in args.ext} if args.ext else set()

    print_tree(
        dir_path=args.path,
        exclude_dirs=exclude_dirs,
        allowed_exts=allowed_exts
    )

if __name__ == "__main__":
    main()