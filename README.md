# Script Utilities (`srcrun`)

A collection of personal utility scripts for general workflow automation and project documentation.

## How It Works

The runner script (`srcrun`) acts as a central execution bridge. When you call `srcrun <script_name>`, it resolves the path to your central script directory and executes `<script_name>.py` using your system's Python interpreter, forwarding any additional command-line arguments.

For example, `srcrun ptree -e venv -x py` executes `ptree.py` while passing `-e venv -x py` directly to Python.

---

## Setup Instructions

### 1. Clone the Repository

Clone the repository to your preferred local directory:

```bash
git clone https://github.com/why-sobi/srcrun.git
cd srcrun

```

### 2. Configure PATH Access

#### Windows (PowerShell)

Run this single command in PowerShell to permanently add the cloned directory to your User PATH variable:

```powershell
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";" + (Get-Location).Path, "User")

```

*Note: Restart any open terminal windows after running this command.*

#### Linux / macOS (Bash / Zsh)

1. Make the launcher script executable:
```bash
chmod +x srcrun

```


2. Add the directory to your shell profile:
```bash
# For Bash:
echo "export PATH=\"\$PATH:$(pwd)\"" >> ~/.bashrc
source ~/.bashrc

# For Zsh (macOS default):
echo "export PATH=\"\$PATH:$(pwd)\"" >> ~/.zshrc
source ~/.zshrc

```



---

## Usage Examples

Once configured, invoke any script from any directory terminal prompt:

* **Run directory visualizer:**
```bash
srcrun ptree

```


* **Pass options to scripts:**
```bash
srcrun ptree -e venv .git -x py md cpp hpp

```


* **Display script help options:**
```bash
srcrun ptree -h

```

---

## Adding New Scripts

To add a new tool:

1. Create your script inside the repository directory (e.g., `my_tool.py`).
2. Run it immediately from any location using `srcrun my_tool`.