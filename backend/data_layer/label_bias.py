def check_label_bias(df, label_col, protected_col):
    grouped = (
        df.groupby(protected_col)[label_col]
        .mean()
        .to_dict()
    )

    return grouped