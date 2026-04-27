def severity_from_di(di):

    if di is None:
        return "unknown"

    if di >= 0.9:
        return "low"

    if di >= 0.8:
        return "moderate"

    if di >= 0.6:
        return "high"

    return "critical"


def severity_from_counterfactual(diff):

    if diff < 0.05:
        return "low"

    if diff < 0.15:
        return "moderate"

    if diff < 0.3:
        return "high"

    return "critical"