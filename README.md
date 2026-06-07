# lynx
lynx: Local Yard for Notes and eXercises. (A lecture management system)

## Install locally

```bash
uv sync
```

## Development setup (uv virtual environment)

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
