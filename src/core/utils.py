# src/core/utils.py
import os, zipfile, shutil

def safe_write_text(path: str, text: str, overwrite: bool = True):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not overwrite and os.path.exists(path):
        raise FileExistsError(f"{path} already exists")
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def extract_zip(zip_path: str, extract_to: str):
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zf:
        zf.extractall(extract_to)
    return extract_to

def remove_dir(path: str):
    if os.path.exists(path):
        shutil.rmtree(path)
