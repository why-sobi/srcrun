import argparse
import fnmatch
from pathlib import Path


# --------------------------------------------------------------------------
# Matching helpers
# --------------------------------------------------------------------------

def _rel_posix(path: Path, root: Path) -> str:
    """Path relative to root, as a forward-slash string (e.g. 'src/utils')."""
    return path.relative_to(root).as_posix()


def _matches(name: str, rel_path: str, patterns: set) -> bool:
    """
    True if a pattern matches either the bare name ('utils') or the full
    relative path ('src/utils'). This lets -id/-ed accept flat names AND
    nested relative paths.
    """
    return any(
        fnmatch.fnmatch(name, pat) or fnmatch.fnmatch(rel_path, pat)
        for pat in patterns
    )


def _is_ancestor_of_pattern(rel_path: str, pattern: str) -> bool:
    """
    True if rel_path is a step on the way to satisfying `pattern`, e.g.
    rel_path='src' is an ancestor of pattern='src/components'.
    Each path segment is compared with fnmatch, so patterns like
    'src/*/models' also work.
    """
    rel_parts = rel_path.split("/")
    pat_parts = pattern.split("/")
    if len(rel_parts) >= len(pat_parts):
        return False
    return all(fnmatch.fnmatch(r, p) for r, p in zip(rel_parts, pat_parts))


# --------------------------------------------------------------------------
# Tree printer
# --------------------------------------------------------------------------

def print_tree(
    dir_path: Path,
    root: Path,
    prefix: str = "",
    exclude_dirs: set = None,
    include_dirs: set = None,
    exclude_files: set = None,
    include_files: set = None,
    include_open: bool = False,
):
    """
    Recursively print a directory tree.

    include_open:
        Once a directory has satisfied an -id pattern (or no -id patterns
        were given at all), this is True and include-dir filtering is
        switched off for everything beneath it -- so opening a matched
        root-level folder doesn't accidentally prune its contents further
        down the tree. While False, only directories that either fully
        match an include pattern, or sit on the path toward one (an
        "ancestor"), are kept -- this is what scopes the initial search
        space without needing to flatten the include patterns to top-level
        names only.
    """
    exclude_dirs = exclude_dirs or set()
    include_dirs = include_dirs or set()
    exclude_files = exclude_files or set()
    include_files = include_files or set()

    # If there are no include-dir filters at all, filtering is trivially "open".
    include_open = include_open or not include_dirs

    items = []  # list of (path, child_include_open) -- child flag only matters for dirs

    for path in dir_path.iterdir():
        rel_path = _rel_posix(path, root)
        name = path.name

        if path.is_dir():
            if _matches(name, rel_path, exclude_dirs):
                continue

            if include_open:
                items.append((path, True))
            else:
                if _matches(name, rel_path, include_dirs):
                    # Fully matched -> open up, no more include filtering below.
                    items.append((path, True))
                elif any(_is_ancestor_of_pattern(rel_path, pat) for pat in include_dirs):
                    # On the way to a match -> keep it visible, keep filtering below.
                    items.append((path, False))
                # else: outside the requested search space entirely -> skip.

        elif path.is_file():
            if _matches(name, rel_path, exclude_files):
                continue
            if include_files and not _matches(name, rel_path, include_files):
                continue
            items.append((path, None))

    items.sort(key=lambda item: (not item[0].is_dir(), item[0].name.lower()))

    count = len(items)
    for i, (item, child_open) in enumerate(items):
        is_last = (i == count - 1)
        connector = "└── " if is_last else "├── "
        print(f"{prefix}{connector}{item.name}")

        if item.is_dir():
            child_prefix = prefix + ("    " if is_last else "│   ")
            print_tree(
                item,
                root=root,
                prefix=child_prefix,
                exclude_dirs=exclude_dirs,
                include_dirs=include_dirs,
                exclude_files=exclude_files,
                include_files=include_files,
                include_open=child_open,
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
        help=(
            "Directory patterns to exclude. Accepts bare names ('venv') "
            "or relative paths ('src/build') to target a specific nested folder."
        )
    )
    parser.add_argument(
        "-id", "--include-dirs",
        nargs="*",
        default=[],
        help=(
            "Directory patterns to restrict the search space to. Accepts bare "
            "names ('src') or relative paths ('src/components'). Ancestor "
            "folders on the way to a match are kept visible; once a match is "
            "reached, everything beneath it is shown normally (no further "
            "pruning)."
        )
    )

    # File controls
    parser.add_argument(
        "-ef", "--exclude-files",
        nargs="*",
        default=["*.pyc", "*.tmp", ".DS_Store"],
        help="File patterns to exclude (e.g. '*.log', 'config.json', 'tests/*.log')"
    )
    parser.add_argument(
        "-if", "--include-files",
        nargs="*",
        default=["*.md", "*.py", "*.hpp", "*.cpp"],
        help="File patterns to include (e.g. '*.py', 'checkpoints/*.pt'). Leave empty to include all non-excluded files."
    )

    args = parser.parse_args()
    root = args.path

    print_tree(
        dir_path=root,
        root=root,
        exclude_dirs=set(args.exclude_dirs),
        include_dirs=set(args.include_dirs),
        exclude_files=set(args.exclude_files),
        include_files=set(args.include_files),
        include_open=False,
    )


if __name__ == "__main__":
    main()