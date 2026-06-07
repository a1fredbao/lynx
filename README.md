# lynx
lynx: Local Yard for Notes and eXercises. (A lecture management system)

It provides a simple CLI interface to manage your lecture notes and exercises. You can easily create, organize, and pack your lecture materials/homework with lynx.

## Installation

### With uv (recommended)

```bash
uv tool install pyLynx
```

### From source

```bash
git clone https://github.com/a1fredbao/lynx
uv tool install .
```

### Development setup (uv virtual environment)

```bash
uv sync --extra dev
pytest
```

`uv sync`/`uv sync --extra dev` will create and manage the project virtual environment automatically.

## CLI usage

```bash
lynx course <course_name>
lynx lecture <lecture_name>
lynx clean
lynx pack
```
