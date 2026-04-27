from fastapi import APIRouter, HTTPException
from backend.data_layer.dataset_loader import load_dataset
from backend.model_audit.probing import probe_model_api

router = APIRouter(prefix="/probe", tags=["probe"])


@router.post("/")
def probe_model(
    filename: str,
    protected: str,
    predict_url: str,
    allow_local_predict_url: bool = False
):
    # prevent path traversal
    if "/" in filename or "\\" in filename:
        raise HTTPException(
            status_code=400,
            detail="Invalid filename"
        )

    try:
        df = load_dataset(filename)
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )

    try:
        results = probe_model_api(
            df,
            protected,
            predict_url,
            allow_private_predict_url=allow_local_predict_url
        )
    except KeyError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Column not found: {str(e)}"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    return results
