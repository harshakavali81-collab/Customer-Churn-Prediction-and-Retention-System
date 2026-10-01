# Results — synthetic demonstration

Selected model: logistic. Training: 3300; validation: 1100; holdout: 1100; current scoring: 1100 customers.

Holdout ROC-AUC: 0.788. Average precision: 0.617 versus prevalence 0.282.
Precision: 57.6%; recall: 49.0%; F1: 0.530; Brier score: 0.160.
Validation-selected threshold: 0.5016. Holdout contact rate: 24.0%. Precision lift: 2.04x.

Current cohort: 270 flagged. Outreach is ranked by risk; an operational team should cap the list to its capacity.

## Interpretation
These metrics measure recovery of the simulator's patterns, not real customer behavior. Contract, usage, support and payment features were deliberately used to generate outcomes. Retention actions are transparent business rules, not causal explanations or proven interventions.

## Next experiment
Randomly assign eligible customers to intervention and control. Predefine 30-day retention, treatment cost, gross margin and complaint guardrails. Estimate treatment-control retention difference with uncertainty. Do not claim revenue saved from predicted risk alone.
