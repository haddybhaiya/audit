from fastapi import APIRouter, HTTPException
from backend.data_layer.dataset_loader import load_dataset
from backend.model_audit.metrics import compute_fairness_metrics
import os

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/")
def audit_model(
    filename: str,
    prediction: str,
    protected: str,
    label: str = None
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
        metrics = compute_fairness_metrics(
            df,
            prediction,
            protected,
            label
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

    return metrics
