from fastapi import APIRouter, HTTPException
from backend.data_layer.dataset_loader import load_dataset
from backend.model_audit.surrogate import run_surrogate_analysis

router = APIRouter(prefix="/surrogate", tags=["surrogate"])


@router.get("/")
def surrogate_analysis(
    filename: str,
    prediction: str,
    protected: str
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
        results = run_surrogate_analysis(
            df,
            prediction,
            protected
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
