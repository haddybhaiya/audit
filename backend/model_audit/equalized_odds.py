from sklearn.metrics import confusion_matrix


def equalized_odds(df, y_true, y_pred, protected_col):
    results = {}

    groups = df[protected_col].unique()

    for g in groups:
        subset = df[df[protected_col] == g]

        y_t = subset[y_true]
        y_p = subset[y_pred]

        cm = confusion_matrix(y_t, y_p, labels=[0, 1])

        # ensure 2x2
        if cm.shape != (2, 2):
            results[g] = {
                "TPR": 0,
                "FPR": 0
            }
            continue

        tn, fp, fn, tp = cm.ravel()

        tpr = tp / (tp + fn) if (tp + fn) else 0
        fpr = fp / (fp + tn) if (fp + tn) else 0

        results[g] = {
            "TPR": float(tpr),
            "FPR": float(fpr)
        }

    return results