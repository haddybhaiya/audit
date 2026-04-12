from backend.utils.correlations import cramers_v

PROXY_DICT = {
    "zip": "race",
    "zipcode": "race",
    "surname": "ethnicity",
    "school": "socioeconomic",
    "college": "wealth",
    "area": "region",
    "city": "region"
}


def scan_name_proxies(df):
    findings = []

    for col in df.columns:
        col_lower = col.lower()

        for keyword, group in PROXY_DICT.items():
            if keyword in col_lower:
                findings.append({
                    "feature": col,
                    "proxy_for": group,
                    "severity": "high",
                    "type": "name_match"
                })

    return findings


def scan_correlation_proxies(df, protected_col):
    findings = []

    for col in df.columns:

        if col == protected_col:
            continue

        try:
            score = cramers_v(df[col], df[protected_col])

            if score > 0.3:
                findings.append({
                    "feature": col,
                    "correlation": float(score),
                    "severity": "high" if score > 0.5 else "medium",
                    "type": "correlation"
                })

        except:
            continue

    return findings