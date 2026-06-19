# lynx

**lynx** (Lectures' Yet aNother eXporter) is a command-line interface (CLI) tool and developer SDK designed to manage lecture notes, exercises, homework templates, and source code submissions.

With lynx, you can easily bootstrap course workspaces, keep them clean, generate syntax-highlighted code snapshots, and bundle your assignments for submission.

---

## Features

- **Workspace Scaffolding**: Scaffold course structures and individual lecture workspaces instantly.
- **Automated Packaging**: Configure custom packaging/build scripts via `pack.py` and run them directly from the CLI.
- **Smart File Exclusion**: Package code while ignoring unwanted files (cache, logs, datasets) using project `.gitignore` files or custom ignore patterns.
- **Code Snapshots**: Capture clean, syntax-highlighted PNG images of specific code lines using custom themes and fonts to embed in assignments or reports.

---

## Installation

### Using `uv` (Recommended)

```bash
uv tool install pyLynx
```

### From Source

```bash
git clone https://github.com/a1fredbao/lynx
cd lynx
uv tool install .
```

### Development Setup

To set up a local development environment:

```bash
uv sync --extra dev
uv run pytest
```

---

## CLI Usage

### 1. Create a Course Workspace
Creates a root directory for a course:
```bash
lynx course <course_name>
```

### 2. Scaffold a Lecture Folder
Generates a structured workspace for a lecture containing standard subfolders (`docs/slides`, `docs/notes`, `src`, `output`, `homework`), a `.gitignore` template, and a preconfigured `pack.py` script:
```bash
lynx lecture <lecture_name>
```

### 3. Clean Workspace Cache
Removes temporary Python cached files (`__pycache__/`, `*.pyc`) and sweeps files under `output/`:
```bash
lynx clean
```

### 4. Pack Submissions
Executes the `make_submission()` function defined inside the local workspace's `pack.py` script:
```bash
lynx pack
```

---

## SDK Usage

Lynx comes with a Python SDK to customize your build pipeline inside `pack.py`.

### 1. `Packer` (Packaging Tool)
The `Packer` class lets you easily define which files and directories to compress into a final submission ZIP package.

```python
from lynx.sdk import Packer

packer = Packer()

# Add a single file (supports relative or absolute paths)
# If no dest_path is provided, it is stored relative to the workspace base dir.
packer.add_file("homework/report.docx", dest_path="Submission_Report.docx")

# Add a folder while preserving its structure and ignoring certain files
# Automatically respects workspace .gitignore rules in addition to custom patterns
packer.add_folder("src/", dest_dir="source_code/", ignore_patterns=["*.csv", "__pycache__"])

# Compile the package into output/Final_Submission.zip
packer.build(output_filename="Final_Submission")
```

### 2. `codesnap` (Code Image Generator)
The `codesnap` function creates syntax-highlighted image snapshots of code file snippets.

```python
from lynx.sdk import codesnap

# Snap lines (10-25) and (3-5) and save as a high-quality PNG image
snap_path = codesnap(
    src_file="src/main.py",
    lines=[(10, 25), (3, 5)],
    output_path="output/core_logic.png",
    theme="monokai",         # Any Pygments-supported theme
    font_name="Fira Code"    # Optional custom font name
)

# You can then add this generated image directly to your Packer package
packer.add_file(snap_path, dest_path="img/core_logic.png")
```

# License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
