import os
import uuid
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter(prefix="/upload", tags=["upload"])

TMP_DIR = Path("/tmp")

@router.post("/")
async def upload_dataset(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Uploaded file must include a filename.")

    safe_name = os.path.basename(file.filename)
    stored_filename = f"{uuid.uuid4().hex}_{safe_name}"
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    file_path = TMP_DIR / stored_filename

    try:
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        with open(file_path, "wb") as f:
            f.write(content)

        df = pd.read_csv(file_path)
    except HTTPException:
        raise
    except pd.errors.EmptyDataError as exc:
        raise HTTPException(status_code=400, detail="CSV file has no rows to parse.") from exc
    except pd.errors.ParserError as exc:
        raise HTTPException(status_code=400, detail="Invalid CSV format in uploaded file.") from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to save uploaded file: {exc}") from exc
    finally:
        await file.close()

    return {
        "filename": stored_filename,
        "original_filename": safe_name,
        "storage_root": str(TMP_DIR),
        "path": str(file_path),
        "content_type": file.content_type,
        "size_bytes": len(content),
        "columns": list(df.columns),
        "rows": len(df)
    }
