import pandas as pd


def generate_counterfactual_pairs(df, protected_col):
    if protected_col not in df.columns:
        raise KeyError(f"Column not found: {protected_col}")

    protected_values = df[protected_col].dropna().unique().tolist()

    if len(protected_values) != 2:
        raise ValueError(
            f"{protected_col} must contain exactly 2 unique values to flip"
        )

    first_value, second_value = protected_values
    flip_map = {
        first_value: second_value,
        second_value: first_value
    }

    pairs = []

    for _, row in df.iterrows():
        base = row.to_dict()
        counterfactual = base.copy()
        counterfactual[protected_col] = flip_map.get(
            counterfactual[protected_col],
            counterfactual[protected_col]
        )
        pairs.append((base, counterfactual))

    return pairs

