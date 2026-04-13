def disparate_impact(df, prediction_col, protected_col):
    grouped = (
        df.groupby(protected_col)[prediction_col]
        .mean()
    )

    if len(grouped) < 2:
        return None

    majority = grouped.max()
    minority = grouped.min()

    di = minority / majority if majority != 0 else 0

    return {
        "group_rates": {
            k: float(v) for k, v in grouped.to_dict().items()
        },
        "disparate_impact": float(di),
        "biased": bool(di < 0.8)
    }