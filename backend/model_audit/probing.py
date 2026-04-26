import requests
import numpy as np
from backend.utils.counterfactuals import generate_counterfactual_pairs


def call_model(predict_url, record):
    response = requests.post(predict_url, json=record)

    if response.status_code != 200:
        raise ValueError("Model API failed")

    data = response.json()

    return float(data["prediction"])


def probe_model_api(df, protected_col, predict_url):

    pairs = generate_counterfactual_pairs(df, protected_col)

    scores_a = []
    scores_b = []

    for base, cf in pairs:

        score_a = call_model(predict_url, base)
        score_b = call_model(predict_url, cf)

        scores_a.append(score_a)
        scores_b.append(score_b)

    return compute_probe_bias(scores_a, scores_b)


def compute_probe_bias(scores_a, scores_b):

    scores_a = np.array(scores_a)
    scores_b = np.array(scores_b)

    mean_a = float(scores_a.mean())
    mean_b = float(scores_b.mean())

    di = min(mean_a, mean_b) / max(mean_a, mean_b)

    diff = abs(mean_a - mean_b)

    return {
        "mean_group_a": mean_a,
        "mean_group_b": mean_b,
        "disparate_impact": float(di),
        "avg_difference": float(diff),
        "bias_detected": bool(di < 0.8)
    }
    