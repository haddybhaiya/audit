import pandas as pd
import os

DATA_DIR = "data"

def load_dataset(filename:str):
    path = os.path.join(DATA_DIR,filename)

    if not os.path.exists(path):
        raise FileNotFoundError(f"{filename} NOT FOUND")
    df = pd.read_csv(path)

    return df


def validate_dataset_filename(filename: str) -> None:
    """Reject filenames containing path separators; mirrors the /probe endpoint's guard."""
    if "/" in filename or "\\" in filename:
        raise ValueError("Invalid filename")
    
