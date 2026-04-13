from backend.model_audit.disparate_impact import disparate_impact
from backend.model_audit.equalized_odds import equalized_odds


def compute_fairness_metrics(
    df,
    prediction_col,
    protected_col,
    label_col=None
):

    metrics = {}

    di = disparate_impact(
        df,
        prediction_col,
        protected_col
    )

    metrics["disparate_impact"] = di

    if label_col:
        eo = equalized_odds(
            df,
            label_col,
            prediction_col,
            protected_col
        )

        metrics["equalized_odds"] = eo

    return metrics