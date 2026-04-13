from sklearn.metrics import confusion_matrix


def equalized_odds(df, y_true, y_pred, protected_col):
    results = {}

    groups = df[protected_col].unique()

    for g in groups:
        subset = df[df[protected_col] == g]

        tn, fp, fn, tp = confusion_matrix(
            subset[y_true],
            subset[y_pred]
        ).ravel()

        tpr = tp / (tp + fn) if (tp + fn) else 0
        fpr = fp / (fp + tn) if (fp + tn) else 0

        results[g] = {
            "TPR": tpr,
            "FPR": fpr
        }

    return results