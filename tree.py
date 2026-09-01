import argparse
import fnmatch
from pathlib import Path

def print_tree(
    dir_path: Path,
    prefix: str = "",
    exclude_dirs: set = None,
    include_dirs: set = None,
    exclude_files: set = None,
    include_files: set = None
):
    exclude_dirs = exclude_dirs or set()
    include_dirs = include_dirs or set()
    exclude_files = exclude_files or set()
    include_files = include_files or set()

    items = []
    for path in dir_path.iterdir():
        if path.is_dir():
            # Exclude directory check
            if any(fnmatch.fnmatch(path.name, pat) for pat in exclude_dirs):
                continue
            # Include directory check (if whitelist passed, only traverse matching dirs)
            if include_dirs and not any(fnmatch.fnmatch(path.name, pat) for pat in include_dirs):
                continue
            items.append(path)
            
        elif path.is_file():
            # Exclude file check
            if any(fnmatch.fnmatch(path.name, pat) for pat in exclude_files):
                continue
            # Include file check (if whitelist passed, show only matching files)
            if include_files and not any(fnmatch.fnmatch(path.name, pat) for pat in include_files):
                continue
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
                include_dirs=include_dirs,
                exclude_files=exclude_files,
                include_files=include_files
            )

def main():
    parser = argparse.ArgumentParser(
        description="Print a visual directory tree with granular directory/file controls."
    )
    
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        type=Path,
        help="Target directory path (default: current directory)"
    )
    
    # Directory controls
    parser.add_argument(
        "-ed", "--exclude-dirs",
        nargs="*",
        default=["venv", ".git", ".vscode", "__pycache__", ".*"],
        help="Directory patterns to exclude (e.g. 'venv', '.*', 'node_modules')"
    )
    parser.add_argument(
        "-id", "--include-dirs",
        nargs="*",
        default=[],
        help="Directory patterns to exclusively include (e.g. 'src', 'tests')"
    )
    
    # File controls
    parser.add_argument(
        "-ef", "--exclude-files",
        nargs="*",
        default=["*.pyc", "*.tmp", ".DS_Store"],
        help="File patterns to exclude (e.g. '*.log', 'config.json')"
    )
    parser.add_argument(
        "-if", "--include-files",
        nargs="*",
        default=["*.md", "*.py", "*.hpp", "*.cpp"],
        help="File patterns to include (e.g. '*.py' '*.md'). Leave empty to include all non-excluded files."
    )

    args = parser.parse_args()

    print_tree(
        dir_path=args.path,
        exclude_dirs=set(args.exclude_dirs),
        include_dirs=set(args.include_dirs),
        exclude_files=set(args.exclude_files),
        include_files=set(args.include_files)
    )

if __name__ == "__main__":
    main()