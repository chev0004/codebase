# Codebase

A simple but powerful command-line tool to consolidate an entire codebase into a single text file, making it easy to paste into Large Language Models (LLMs) like Claude, Gemini, or ChatGPT.

## Features

- **Intelligent Ignoring**: Automatically respects rules in `.gitignore` files.  
- **Smart Defaults**: Ignores common nuisance files (`.git`, `__pycache__`) even without a `.gitignore`.  
- **Flexible**: Specify which project directory to scan.  
- **Customizable Output**: Choose the name for the combined file.  
- **Progress Tracking**: A clean progress bar shows you which files are being processed.

## Installation

There are two easy ways to install Codebase Combiner.

### Option 1: Direct Install from GitHub (Recommended)

You can install the tool directly from this repository using `pip`. This is the quickest way to get started.

```bash
pip install git+https://github.com/chev0004/codebase.git
```

### Option 2: Clone and Install Locally

If you prefer to have the source code on your machine, you can clone the repository first.

1. Clone the repository:
    ```bash
    git clone https://github.com/chev0004/codebase.git
    cd codebase
    ```
2. Install the project:
    ```bash
    pip install .
    ```

After installation, the `codebase` command will be available automatically in your terminal. You can run it from any directory.

## Usage

Run the script from your terminal, pointing it to the project directory you want to combine.

**Basic Usage (combines the current directory):**
```bash
codebase.py .
```

**Specify an output file name:**
```bash
codebase.py . --output my_project.md
```
