import pandas as pd
import os

DATA_DIR = "data"

def load_dataset(filename:str):
    path = os.path.join(DATA_DIR,filename)

    if not os.path.exists(path):
        raise FileNotFoundError(f"{filename} NOT FOUND")
    df = pd.read_csv(path)

    return df
    
