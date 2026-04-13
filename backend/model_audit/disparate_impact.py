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
        "group_rates": grouped.to_dict(),
        "disparate_impact": float(di),
        "biased": di < 0.8
    }