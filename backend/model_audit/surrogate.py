import pandas as pd
from sklearn.tree import DecisionTreeRegressor


def train_surrogate_model(
    df,
    feature_cols,
    prediction_col,
    max_depth=3
):

    X = df[feature_cols]
    y = df[prediction_col]

    # encode categorical features
    X_encoded = pd.get_dummies(X)

    model = DecisionTreeRegressor(
        max_depth=max_depth
    )

    model.fit(X_encoded, y)

    return model, X_encoded.columns.tolist()


def surrogate_feature_importance(
    model,
    encoded_cols
):

    importances = model.feature_importances_

    return {
        feature: float(score)
        for feature, score in zip(
            encoded_cols,
            importances
        )
    }
def run_surrogate_analysis(
    df,
    prediction_col,
    protected_col
):
    if prediction_col not in df.columns:
        raise KeyError(prediction_col)
    if protected_col not in df.columns:
        raise KeyError(protected_col)

    feature_cols = [
        col for col in df.columns
        if col != prediction_col
    ]

    model, encoded_cols = train_surrogate_model(
        df,
        feature_cols,
        prediction_col
    )

    importance = surrogate_feature_importance(
        model,
        encoded_cols
    )

    # aggregate protected importance
    protected_importance = sum(
        score
        for col, score in importance.items()
        if protected_col in col
    )

    return {
        "feature_importance": importance,
        "protected_feature_importance":
            float(protected_importance)
    }

