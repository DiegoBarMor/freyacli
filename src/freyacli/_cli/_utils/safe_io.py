from pathlib import Path

# ------------------------------------------------------------------------------
def safe_read_file(path: Path) -> str:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        if not path.is_file():
            raise IsADirectoryError(f"Path is not a file: {path}")
        with open(path, 'r') as f:
            return f.read()


# ------------------------------------------------------------------------------
