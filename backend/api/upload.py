from fastapi import  APIRouter, UploadFile,File
import pandas as pd
import os

router  = APIRouter(prefix="/upload", tags=["upload"])

DATA_DIR = "data"

@router.post("/")
async def upload_dataset(file: UploadFile = File(...)):
    os.makedirs(DATA_DIR, exist_ok=True)
    file_path = os.path.join(DATA_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())
    
    df = pd.read_csv(file_path)

    return{
        "filename": file.filename,
        "columns": list(df.columns),
        "rows": len(df)

    }
    