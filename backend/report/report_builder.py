from backend.report.severity_mapper import (
    severity_from_di,
    severity_from_counterfactual
)

from backend.report.bias_summary import generate_bias_summary


def build_bias_report(
    audit_results,
    probe_results,
    surrogate_results
):

    di = audit_results["disparate_impact"]["disparate_impact"]

    counterfactual_diff = probe_results.get(
        "avg_counterfactual_difference"
    )
    if counterfactual_diff is None:
        counterfactual_diff = probe_results.get("avg_difference")
    if counterfactual_diff is None:
        raise KeyError("avg_counterfactual_difference")

    protected_importance = surrogate_results[
        "protected_feature_importance"
    ]

    summary = generate_bias_summary(
        di,
        counterfactual_diff,
        protected_importance
    )

    return {
        "severity": {
            "group_bias":
                severity_from_di(di),

            "counterfactual_bias":
                severity_from_counterfactual(
                    counterfactual_diff
                )
        },
        "summary": summary,
        "metrics": {
            "disparate_impact": di,
            "counterfactual_difference":
                counterfactual_diff,
            "protected_importance":
                protected_importance
        }
    }
