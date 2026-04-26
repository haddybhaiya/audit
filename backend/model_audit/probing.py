import requests
import numpy as np
from urllib.parse import urlparse
import ipaddress
import socket
import os
from backend.utils.counterfactuals import generate_counterfactual_pairs


def _validate_predict_url(predict_url):
    allow_private = os.getenv("AUDIT_ALLOW_PRIVATE_PREDICT_URLS") == "1"
    parsed = urlparse(predict_url)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError("predict_url must use http or https")

    if not parsed.hostname:
        raise ValueError("predict_url must include a valid host")

    forbidden_hosts = {"localhost"}
    hostname = parsed.hostname.lower()

    if hostname in forbidden_hosts and not allow_private:
        raise ValueError("predict_url host is not allowed")

    try:
        addresses = {
            result[4][0]
            for result in socket.getaddrinfo(parsed.hostname, None)
        }
    except socket.gaierror as e:
        raise ValueError("predict_url host could not be resolved") from e

    for addr in addresses:
        ip = ipaddress.ip_address(addr)
        if (
            ip.is_private or ip.is_loopback or ip.is_link_local or
            ip.is_multicast or ip.is_reserved or ip.is_unspecified
        ) and not allow_private:
            raise ValueError("predict_url resolves to a non-public address")


def call_model(predict_url, record):
    try:
        response = requests.post(predict_url, json=record, timeout=10)
    except requests.RequestException as e:
        raise ValueError(f"Model API request failed: {e}") from e

    if response.status_code != 200:
        raise ValueError("Model API failed")

    try:
        data = response.json()
    except ValueError as e:
        raise ValueError("Model API returned invalid JSON") from e

    if "prediction" not in data:
        raise ValueError("Model API response missing 'prediction'")

    return float(data["prediction"])


def probe_model_api(df, protected_col, predict_url):
    _validate_predict_url(predict_url)

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

    if mean_a == 0 and mean_b == 0:
        di = 1.0
    else:
        di = min(mean_a, mean_b) / max(mean_a, mean_b)

    diff = abs(mean_a - mean_b)

    return {
        "mean_group_a": mean_a,
        "mean_group_b": mean_b,
        "disparate_impact": float(di),
        "avg_difference": float(diff),
        "bias_detected": bool(di < 0.8)
    }
    
