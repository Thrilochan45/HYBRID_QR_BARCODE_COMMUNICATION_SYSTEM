import os
from config import OUTPUT_DIR

def ensure_path(path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)

def output_path(filename: str) -> str:
    out = os.path.join(OUTPUT_DIR, filename)
    ensure_path(out)
    return out
