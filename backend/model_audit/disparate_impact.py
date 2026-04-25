def disparate_impact(df, prediction_col, protected_col):
    grouped = (
        df.groupby(protected_col)[prediction_col]
        .mean()
    )

    if len(grouped) < 2:
        return None

    majority = float(grouped.max())
    minority = float(grouped.min())

    # handle undefined case (all zero)
    if majority == 0 and minority == 0:
        di = 1.0
    else:
        di = minority / majority if majority != 0 else 0

    return {
        "group_rates": {
            str(k): float(v)
            for k, v in grouped.to_dict().items()
        },
        "disparate_impact": float(di),
        "biased": bool(di < 0.8)
    }