from backend.model_audit.disparate_impact import disparate_impact
from backend.model_audit.equalized_odds import equalized_odds


def compute_fairness_metrics(
    df,
    prediction_col,
    protected_col,
    label_col=None
):

    metrics = {}

    metrics["disparate_impact"] = disparate_impact(
        df,
        prediction_col,
        protected_col
    )

    if label_col is not None:
        metrics["equalized_odds"] = equalized_odds(
            df,
            label_col,
            prediction_col,
            protected_col
        )

    return metrics