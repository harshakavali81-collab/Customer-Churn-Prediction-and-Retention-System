# Customer Churn Prediction and Retention System

A reproducible portfolio project by Kavali Harshavardhan, built with Python, SQL, scikit-learn and Streamlit. Predicts 30-day cancellation risk, ranks an outreach queue and suggests rule-based retention actions.

[Setup](#local-installation--setup-guide) · [Architecture](#architecture--system-design-diagram) · [Detailed guide](PROJECT_GUIDE.md) · [Repository standard](docs/REPOSITORY_STANDARD.md)

## Visuals

![Model performance](<reports/model_performance.png>)

Existing project visual; diagrams and illustrative graphics are not evidence of a deployed application.

## Live Link / Demo

[Open Customer Retention Studio](https://harsha-customer-retention.kavaliharshavardhan9.chatgpt.site) (public access). The browser companion includes batch CSV and single-customer scoring, a capacity-limited outreach queue, model evaluation and the PDF guide. The Python project remains available for training, Streamlit and monitoring.

Read [the architecture and workflow](docs/ARCHITECTURE.md) and [completion status](docs/COMPLETION.md).

## Key Features

- Source and supporting materials indexed in [Repository standard](docs/REPOSITORY_STANDARD.md).
- Detailed methodology and project context in [Project guide](PROJECT_GUIDE.md).

## Tech Stack

![Python](https://img.shields.io/badge/Python-334155?style=flat-square) ![Streamlit](https://img.shields.io/badge/Streamlit-334155?style=flat-square) ![scikit-learn](https://img.shields.io/badge/scikit--learn-334155?style=flat-square) ![Pandas](https://img.shields.io/badge/Pandas-334155?style=flat-square) ![NumPy](https://img.shields.io/badge/NumPy-334155?style=flat-square) ![SQL](https://img.shields.io/badge/SQL-334155?style=flat-square) ![Docker](https://img.shields.io/badge/Docker-334155?style=flat-square)

Dependency versions and optional packages are defined in the repository manifests.

## Architecture / System Design Diagram

[Architecture documentation / diagram](<docs/ARCHITECTURE.md>)

## Local Installation & Setup Guide

```bash
git clone https://github.com/harshakavali81-collab/Customer-Churn-Prediction-and-Retention-System.git
cd Customer-Churn-Prediction-and-Retention-System
```

1. Extract the ZIP and open this folder in VS Code.
2. Install Python 3.11 or 3.12. Open Terminal → New Terminal.
3. Run:
```powershell
py -3.11 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python -m streamlit run app.py
```
If you installed Python 3.12, replace `-3.11` with `-3.12`. A trained model and generated outputs are already included. Open the localhost URL printed in the terminal.

To reproduce everything and run tests:
```powershell
.venv\Scripts\python -m src.pipeline
.venv\Scripts\python -m unittest discover -s tests -v
```

macOS/Linux:
```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m src.pipeline
.venv/bin/python -m streamlit run app.py
```

## Challenges & Solutions

Churn means cancellation in the 30 days following the snapshot. Usage_previous and usage_current are the two 30-day windows ending before the snapshot. Billing failures and support tickets also describe the preceding 30 days. The outcome is never used as an input.

There are 6,600 unique customers across six cohorts, plus 20 exact duplicates in the raw source. Each customer appears once. Jan/Mar/May train, July validates, September tests, November simulates a scoring cohort. Two-month gaps ensure the 30-day outcome window closes before the next split. Median/mode imputation and encoding fit on training only. No resampling is needed for the simulated class distribution.

Compare Dummy, Logistic Regression, Random Forest and Histogram Gradient Boosting by validation average precision. Select a threshold that flags no more than 20% of validation customers, then evaluate once on the test set. Contact volume on new cohorts can differ; use the app's capacity limit. The shipped model is the evaluated training-only model, without later refitting.

Risk bands are descriptive (<30%, 30–60%, >60%) and independent of the contact cutoff. Actions use observed rules in priority order: billing failure, repeated support tickets, usage decline, then general needs review. They are not per-customer feature attributions. Global permutation importance is measured on validation data.

## Future Improvements

- Capture a reproducible end-to-end demo with runtime versions and sample inputs.
- Expand regression checks for invalid inputs and documented edge cases.
- Record measured results, data provenance and deployment limitations alongside each release.

## Scope and supporting evidence

A reproducible portfolio project by Kavali Harshavardhan, built with Python, SQL, scikit-learn and Streamlit. Predicts 30-day cancellation risk, ranks an outreach queue and suggests rule-based retention actions.

**Data: entirely synthetic. No real customer records or measured business impact.** The simulator intentionally links usage, contract and billing patterns with churn. Model scores demonstrate technical execution and do not establish real-world performance.

Read [the complete illustrated PDF guide](docs/Customer_Churn_Project_Complete_Guide.pdf) for the workflow, results, setup and interview explanation.

## Repository Structure

| Location | Purpose |
| --- | --- |
| `src/` | Source modules |
| `tests/` | Tests |
| `docs/` | Documentation |
| `data/` | Data and samples |
| `sql/` | SQL schema and analysis |
| `.github/` | Issue forms, PR template and automated checks |

[Complete file inventory and workflow](docs/REPOSITORY_STANDARD.md). Runtime entry points retain their existing paths.

## Workflow & Tracking

Use the [bug and feature forms](https://github.com/harshakavali81-collab/Customer-Churn-Prediction-and-Retention-System/issues/new/choose) to define work with acceptance criteria. Keep tasks in Todo → In progress → Review → Done, and link a pull request with `Closes #<number>`. See [the maintenance workflow](docs/REPOSITORY_STANDARD.md#workflow).

## License

Original project software is available under the [MIT License](LICENSE). See [licensing scope](docs/LICENSING.md) for third-party and data exclusions.

