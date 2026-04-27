from fastapi import APIRouter, HTTPException

from backend.data_layer.dataset_loader import load_dataset
from backend.model_audit.metrics import compute_fairness_metrics
from backend.model_audit.probing import run_probing_engine
from backend.model_audit.surrogate import run_surrogate_analysis
from backend.report.report_builder import build_bias_report

router = APIRouter(prefix="/report", tags=["report"])


@router.post("/")
def generate_report(
    filename: str,
    prediction: str,
    protected: str,
    predict_url: str,
    allow_local_predict_url: bool = False
):

    try:
        df = load_dataset(filename)

        audit = compute_fairness_metrics(
            df,
            prediction,
            protected
        )

        probe = run_probing_engine(
            df,
            predict_url,
            protected,
            allow_private_predict_url=allow_local_predict_url
        )

        surrogate = run_surrogate_analysis(
            df,
            prediction,
            protected
        )

        report = build_bias_report(
            audit,
            probe,
            surrogate
        )

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    return report
