from fastapi import APIRouter
from backend.data_layer.dataset_loader import load_dataset
from backend.model_audit.metrics import compute_fairness_metrics

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/")
def audit_model(
    filename: str,
    prediction: str,
    protected: str,
    label: str = None
):

    df = load_dataset(filename)

    metrics = compute_fairness_metrics(
        df,
        prediction,
        protected,
        label
    )

    return metrics