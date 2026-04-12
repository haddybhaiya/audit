def check_balance(df,protected_col):
    distribution = (
        df[protected_col]
        .value_counts(normalize=True)
        .reset_index()

    )
    return distribution
