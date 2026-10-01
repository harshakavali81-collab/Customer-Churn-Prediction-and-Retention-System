# Model card
Purpose: educational subscription churn prioritization for a 30-day horizon.
Population: synthetic subscription customers. No protected attributes or personal identifiers beyond artificial IDs.
Intended user: portfolio reviewer or analyst running a local demonstration.
Not intended for: production targeting, credit eligibility, cancellation denial or pricing decisions.

Selection: validation average precision. Test results: `reports/metrics.json`. AP is reported as average precision, not trapezoidal PR-AUC. ROC-AUC, precision, recall, F1, Brier and confusion matrix accompany it. Brier score measures probabilistic error; explicit calibration is not implemented. The majority baseline is included for comparison.

Chronological validation uses distinct customer IDs and a matured outcome gap. Imputation and preprocessing fit only on training. Cohort randomness comes from a single reproducible simulator, so measured stability does not prove robustness to real distribution shifts. One split and one seed do not establish confidence intervals.

Threshold: choose a strict cutoff above the validation 80th percentile boundary, allowing at most 20% outreach in validation. New data can exceed that rate. For capacity planning take the highest-ranked eligible customers up to the operational limit.

Monitoring: `python -m src.monitor --input data/current_customers.csv` compares missing rates and numeric distributions with training, plus categorical schema validation. These heuristics flag review, not proof of performance decay. Optional `--labels` accepts customer_id, actual; labels must cover the full input cohort and a completed 30-day window. Monitor performance only after outcome maturity. Retraining requires refreshed data, validation and approval by the model owner.

Security: joblib uses pickle internally; load only the model you generated or trust. This app never accepts model-file uploads. Do not expose real customers via this unauthenticated demo. Production requires authentication, authorization, retention controls, TLS, monitoring, deployment hardening and campaign-consent rules.
