# D:\scripts\install.py
import argparse
import subprocess
import sys
from pathlib import Path

# Locate the root scripts directory relative to this file
SCRIPTS_DIR = Path(__file__).parent.resolve()
REQUIREMENTS_FILE = SCRIPTS_DIR / "requirements.txt"


def run_pip(args: list[str]) -> int:
    """Executes pip using the current virtual environment's Python executable."""
    cmd = [sys.executable, "-m", "pip"] + args
    result = subprocess.run(cmd)
    return result.returncode


def install_packages(packages: list[str]) -> None:
    print(f"Installing packages: {', '.join(packages)}...\n")
    code = run_pip(["install"] + packages)
    if code == 0:
        print("\n[Packages installed successfully!]")
    else:
        print("\n[Failed to install packages.]")


def install_from_requirements() -> None:
    if not REQUIREMENTS_FILE.exists():
        print(f"[Error: {REQUIREMENTS_FILE.name} not found in {SCRIPTS_DIR}]")
        sys.exit(1)

    print(f"Installing dependencies from {REQUIREMENTS_FILE}...\n")
    code = run_pip(["install", "-r", str(REQUIREMENTS_FILE)])
    if code == 0:
        print("\n[Requirements installed successfully!]")
    else:
        print("\n[Failed to install requirements.]")


def freeze_requirements() -> None:
    print(f"Exporting installed packages to {REQUIREMENTS_FILE.name}...")
    try:
        req_data = subprocess.check_output(
            [sys.executable, "-m", "pip", "freeze"]
        ).decode("utf-8")
        REQUIREMENTS_FILE.write_text(req_data, encoding="utf-8")
        print(f"\n[Successfully updated {REQUIREMENTS_FILE}]")
    except subprocess.CalledProcessError:
        print("\n[Failed to generate requirements.txt.]")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="srcrun install",
        description="Manage packages and dependencies for the srcrun virtual environment.",
    )

    # Place positional packages outside the mutually exclusive group
    parser.add_argument(
        "packages",
        nargs="*",
        metavar="PACKAGE",
        default=[],
        help="One or more package names to install (e.g., requests rich pandas)",
    )

    # Create mutually exclusive flags for -r and -f
    flags_group = parser.add_mutually_exclusive_group()

    flags_group.add_argument(
        "-r",
        "--requirements",
        action="store_true",
        help="Install dependencies from requirements.txt",
    )

    flags_group.add_argument(
        "-f",
        "--freeze",
        action="store_true",
        help="Export currently installed packages to requirements.txt",
    )

    args = parser.parse_args()

    # Prevent combining package names with -r or -f
    if args.packages and (args.requirements or args.freeze):
        parser.error("Cannot combine package names with -r/--requirements or -f/--freeze flags.")

    # Route execution
    if args.requirements:
        install_from_requirements()
    elif args.freeze:
        freeze_requirements()
    elif args.packages:
        install_packages(args.packages)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()