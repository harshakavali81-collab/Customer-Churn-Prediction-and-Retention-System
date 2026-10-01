# Interview preparation
## 60-second explanation
I built a customer churn prediction and retention demonstration using Python, SQL, scikit-learn and Streamlit. I generated a reproducible synthetic subscription dataset with missing values and duplicates, defined a 30-day cancellation target, and separated customers chronologically into training, validation and test cohorts. I compared a baseline with three machine-learning models using average precision, selected an outreach threshold on validation data, and evaluated on a held-out cohort. The dashboard supports batch CSV scoring, a ranked outreach queue and rule-based retention recommendations. I also documented limitations: synthetic performance is not evidence of real business impact, and retention actions need controlled experiments.

## Questions to prepare
- Why average precision? It evaluates positive-case ranking and is useful alongside prevalence when positives are less common; accuracy can conceal missed churners.
- How did you prevent leakage? Features predate the snapshot; outcome is excluded; preprocessing fits training only; IDs do not cross splits; 30-day labels mature before subsequent cohorts.
- Why not always use 0.5? Operational capacity matters. The validation cutoff targets at most 20% outreach; the UI enforces a chosen current-batch queue size.
- Why no SMOTE? The simulator does not require it; introducing it without demonstrated benefit adds complexity. Any resampling would belong inside training folds only.
- Does high risk mean an offer will work? No. Risk is different from treatment effect. Randomized intervention/control testing is needed.
- How would you improve it? Real as-of event data, grouped temporal validation, calibration checks, confidence intervals, subgroup evaluation and treatment uplift experiments.

## Resume bullets (use after reviewing and running the project)
- Built a Python and SQL churn prediction pipeline on 6,600 synthetic customer records, with chronological validation, leakage controls and comparison of three ML models against a baseline.
- Developed a Streamlit dashboard for CSV scoring, customer risk segmentation and capacity-limited retention outreach; documented model performance and monitoring limitations.

Read reports/RESULTS.md for measured metrics. Never describe this simulator as real company work or claim retention/revenue improvements that were not measured.

## Five-minute demo
1. State the 30-day business problem and synthetic provenance.
2. Open Overview, filter contracts, adjust outreach capacity and download a queue.
3. Show the sample CSV and score a batch.
4. Show the model comparison, holdout curves and validation feature importance.
5. Explain leakage controls, business action rules and the experiment needed to demonstrate impact.
