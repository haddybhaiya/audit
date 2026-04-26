from fastapi import APIRouter, HTTPException
from backend.data_layer.dataset_loader import load_dataset
from backend.model_audit.probing import probe_model_api

router = APIRouter(prefix="/probe", tags=["probe"])


@router.post("/")
def probe_model(
    filename: str,
    protected: str,
    predict_url: str
):

    try:
        df = load_dataset(filename)

        results = probe_model_api(
            df,
            protected,
            predict_url
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    return results