# Repository standard

## Layout

This repository keeps its working source paths. A shared portfolio structure does not require moving a React application, Python package, BI workbook or Verilog project into identical runtime directories.

| Area | Convention |
| --- | --- |
| Landing page | `README.md`: purpose, visuals, demo, features, stack, architecture, setup, tradeoffs and roadmap |
| Detailed reference | `PROJECT_GUIDE.md`: retained project-specific explanation and historical release notes |
| Documentation | `docs/`: design, inventory, reproduction and evidence |
| Work intake | `.github/ISSUE_TEMPLATE/`: bug and feature forms |
| Review | `.github/PULL_REQUEST_TEMPLATE.md`: linked issue, behavior and validation |
| Automation | `.github/workflows/portfolio-docs.yml`: README section and local-link checks |
| Source and tests | Existing project-specific paths listed below; no empty source/test placeholders |

## Workflow

1. Open an issue describing the user problem and measurable acceptance criteria.
2. Add it to a GitHub Project with Todo, In progress, Review and Done states when a board is configured.
3. Use a focused branch and meaningful commits, such as `docs: correct local setup paths` or `fix(api): reject malformed input`.
4. Run the project's documented checks and `python scripts/check_portfolio_docs.py`.
5. Open a pull request with actual validation results and `Closes #<issue-number>`.
6. Merge after review; record release evidence and update the issue/board.

Board creation, profile pins, repository social previews and milestone settings require account-level configuration. This file does not claim those settings have been applied.

## Validation scope

The documentation check validates the landing-page headings and local link targets only. It does not execute models, certify test coverage, inspect Git history for secrets, verify external websites, or prove production readiness. Existing application workflows remain the source of runtime CI evidence.

Keep credentials in local environment variables. A gitignore rule does not remove secrets already tracked or committed. Use only permitted sample data in public demos.

## Inventory at standardization

The following are the pre-existing public project files. New standardization files are described above. Historical guides may mention external bundles that are not part of this list.

- [`Dockerfile`](<../Dockerfile>)
- [`README.md`](<../README.md>)
- [`START_HERE.txt`](<../START_HERE.txt>)
- [`app.py`](<../app.py>)
- [`browser-demo`](<../browser-demo>)
- [`browser-demo/README.md`](<../browser-demo/README.md>)
- [`browser-demo/dist`](<../browser-demo/dist>)
- [`browser-demo/dist/app.mjs`](<../browser-demo/dist/app.mjs>)
- [`browser-demo/dist/core.mjs`](<../browser-demo/dist/core.mjs>)
- [`browser-demo/dist/data.json`](<../browser-demo/dist/data.json>)
- [`browser-demo/dist/index.html`](<../browser-demo/dist/index.html>)
- [`browser-demo/dist/model.json`](<../browser-demo/dist/model.json>)
- [`browser-demo/dist/model_performance.png`](<../browser-demo/dist/model_performance.png>)
- [`browser-demo/dist/parity.json`](<../browser-demo/dist/parity.json>)
- [`browser-demo/dist/project-guide.pdf`](<../browser-demo/dist/project-guide.pdf>)
- [`browser-demo/dist/sample_customers.csv`](<../browser-demo/dist/sample_customers.csv>)
- [`browser-demo/dist/style.css`](<../browser-demo/dist/style.css>)
- [`browser-demo/test-parity.mjs`](<../browser-demo/test-parity.mjs>)
- [`data`](<../data>)
- [`data/churn.db`](<../data/churn.db>)
- [`data/current_customers.csv`](<../data/current_customers.csv>)
- [`data/customer_scores.csv`](<../data/customer_scores.csv>)
- [`data/customers_clean.csv`](<../data/customers_clean.csv>)
- [`data/customers_raw.csv`](<../data/customers_raw.csv>)
- [`data/retention_outreach.csv`](<../data/retention_outreach.csv>)
- [`docs`](<../docs>)
- [`docs/ARCHITECTURE.md`](<../docs/ARCHITECTURE.md>)
- [`docs/COMPLETION.md`](<../docs/COMPLETION.md>)
- [`docs/Customer_Churn_Project_Complete_Guide.pdf`](<../docs/Customer_Churn_Project_Complete_Guide.pdf>)
- [`docs/DATA_DICTIONARY.md`](<../docs/DATA_DICTIONARY.md>)
- [`docs/GITHUB_AND_DEPLOYMENT.md`](<../docs/GITHUB_AND_DEPLOYMENT.md>)
- [`docs/INTERVIEW_AND_RESUME.md`](<../docs/INTERVIEW_AND_RESUME.md>)
- [`docs/MODEL_CARD.md`](<../docs/MODEL_CARD.md>)
- [`docs/POWER_BI.md`](<../docs/POWER_BI.md>)
- [`models`](<../models>)
- [`models/churn_model.joblib`](<../models/churn_model.joblib>)
- [`notebooks`](<../notebooks>)
- [`notebooks/01_analysis.ipynb`](<../notebooks/01_analysis.ipynb>)
- [`publish_github.ps1`](<../publish_github.ps1>)
- [`reports`](<../reports>)
- [`reports/RESULTS.md`](<../reports/RESULTS.md>)
- [`reports/VERIFICATION.md`](<../reports/VERIFICATION.md>)
- [`reports/data_quality.json`](<../reports/data_quality.json>)
- [`reports/eda.png`](<../reports/eda.png>)
- [`reports/feature_importance.csv`](<../reports/feature_importance.csv>)
- [`reports/metrics.json`](<../reports/metrics.json>)
- [`reports/model_comparison_validation.csv`](<../reports/model_comparison_validation.csv>)
- [`reports/model_performance.png`](<../reports/model_performance.png>)
- [`reports/monitoring.json`](<../reports/monitoring.json>)
- [`reports/sql_result_1.csv`](<../reports/sql_result_1.csv>)
- [`reports/sql_result_2.csv`](<../reports/sql_result_2.csv>)
- [`reports/sql_result_3.csv`](<../reports/sql_result_3.csv>)
- [`reports/sql_result_4.csv`](<../reports/sql_result_4.csv>)
- [`reports/test_ids.csv`](<../reports/test_ids.csv>)
- [`reports/test_predictions.csv`](<../reports/test_predictions.csv>)
- [`reports/train_ids.csv`](<../reports/train_ids.csv>)
- [`reports/validation_ids.csv`](<../reports/validation_ids.csv>)
- [`requirements.txt`](<../requirements.txt>)
- [`sql`](<../sql>)
- [`sql/analysis.sql`](<../sql/analysis.sql>)
- [`src`](<../src>)
- [`src/__init__.py`](<../src/__init__.py>)
- [`src/core.py`](<../src/core.py>)
- [`src/export_browser.py`](<../src/export_browser.py>)
- [`src/monitor.py`](<../src/monitor.py>)
- [`src/pipeline.py`](<../src/pipeline.py>)
- [`tests`](<../tests>)
- [`tests/test_project.py`](<../tests/test_project.py>)
