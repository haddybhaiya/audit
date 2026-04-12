# audit
Audit is an open, end-to-end AI bias detection and analyze platform designed for organizations deploying automated decision systems in high-stakes domains — hiring, credit, healthcare, and criminal justice

## repo structure
```
fairsight/
│
├── backend/
│   ├── main.py
│   ├── config.py
│
│   ├── data_layer/
│   │   ├── dataset_loader.py
│   │   ├── proxy_scanner.py
│   │   ├── balance_checker.py
│   │   └── label_bias.py
│
│   ├── model_audit/
│   │   ├── metrics.py
│   │   ├── disparate_impact.py
│   │   ├── equalized_odds.py
│   │   ├── probing.py
│   │   ├── shap_explainer.py
│   │   └── surrogate.py
│
│   ├── monitoring/
│   │   ├── rolling_metrics.py
│   │   ├── psi.py
│   │   ├── drift_detector.py
│   │   └── feedback_loop.py
│
│   ├── report/
│   │   ├── gemini_report.py
│   │   ├── severity_mapper.py
│   │   └── pdf_export.py
│
│   ├── api/
│   │   ├── upload.py
│   │   ├── scan.py
│   │   ├── audit.py
│   │   ├── monitor.py
│   │   └── report.py
│
│   └── utils/
│       ├── stats.py
│       └── correlations.py
│
├── frontend/
│
├── data/
├── scripts/
├── tests/
│
├── requirements.txt
├── .gitignore
└── README.md

```

## flow 
```
Dataset Upload
      ↓
Data Layer
(proxy detection)
      ↓
Model Audit Layer
(fairness metrics)
      ↓
Black-box probing
      ↓
Report generator
      ↓
Live monitoring
```

