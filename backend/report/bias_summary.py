def generate_bias_summary(
    di,
    counterfactual_diff,
    protected_feature_importance
):

    summary = {}

    if di < 0.8:
        summary["group_bias"] = True
    else:
        summary["group_bias"] = False

    if counterfactual_diff > 0.15:
        summary["counterfactual_bias"] = True
    else:
        summary["counterfactual_bias"] = False

    if protected_feature_importance > 0.2:
        summary["feature_bias"] = True
    else:
        summary["feature_bias"] = False

    return summary