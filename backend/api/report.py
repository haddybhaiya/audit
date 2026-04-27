import os
from pathlib import Path
from typing import Any

import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.model_audit.metrics import compute_fairness_metrics
from backend.model_audit.probing import run_probing_engine
from backend.model_audit.surrogate import run_surrogate_analysis
from backend.report.report_builder import build_bias_report

router = APIRouter(prefix="/report", tags=["report"])
TMP_DIR = Path("/tmp")


class ReportRequest(BaseModel):
    filename: str
    prediction: str
    protected: str
    predict_url: str
    allow_local_predict_url: bool = False


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if type(value).__module__.startswith("numpy"):
        if hasattr(value, "item"):
            return value.item()
        if hasattr(value, "tolist"):
            return value.tolist()
    return value


@router.post("/")
def generate_report(request: ReportRequest):
    file_path = TMP_DIR / os.path.basename(request.filename)
    try:
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Uploaded file not found in /tmp: {os.path.basename(request.filename)}"
            )

        df = pd.read_csv(file_path)

        audit = compute_fairness_metrics(
            df,
            request.prediction,
            request.protected
        )

        probe = run_probing_engine(
            df,
            str(request.predict_url),
            request.protected,
            allow_private_predict_url=request.allow_local_predict_url
        )

        surrogate = run_surrogate_analysis(
            df,
            request.prediction,
            request.protected
        )

        report = build_bias_report(
            audit,
            probe,
            surrogate
        )
        return _json_safe(report)

    except HTTPException:
        raise
    except pd.errors.EmptyDataError as exc:
        raise HTTPException(
            status_code=400,
            detail="Uploaded CSV file is empty or unreadable."
        ) from exc
    except pd.errors.ParserError as exc:
        raise HTTPException(
            status_code=400,
            detail="Uploaded CSV has invalid format."
        ) from exc
    except KeyError as exc:
        missing_column = str(exc).strip("'")
        raise HTTPException(
            status_code=400,
            detail=f"Missing required column: {missing_column}"
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid report input: {exc}"
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate report: {exc}"
        ) from exc
