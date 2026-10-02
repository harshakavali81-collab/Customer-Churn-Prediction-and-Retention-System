# Project completion - 1 October 2026

## Delivered
- Reproducible Python training, SQL analysis and monitoring.
- 6,600 unique synthetic customers, a trained model, evaluation, scores and an outreach queue.
- Streamlit dashboard and a hosted browser companion.
- Full 14-page PDF guide, architecture diagrams, data dictionary, model card and interview notes.
- Public GitHub source and downloadable project ZIP.

## Hosted demo
https://harsha-customer-retention.kavaliharshavardhan9.chatgpt.site

This Site was deployed successfully with owner-private access. It is available to the owner; public visitor access has not been enabled. The source repository remains public. The static browser version implements the fitted Logistic Regression scoring pipeline; it is not a hosted Python/Streamlit process. Uploads are processed in browser memory.

## Verification
The original hosted GitHub Actions training/tests run passed. All nine Python tests passed locally again. Browser predictions match Python across 1,103 records, including missing values and zero usage; maximum absolute difference was 2.22e-16. CSV parsing and input validation tests passed. The updated GitHub workflow now includes these parity checks.

Supported browser preview tooling was unavailable, so visual browser QA and optional WebMCP registration validation were not performed. The deployment service confirmed successful publication. Docker was supplied but not built.

## Scope boundaries
All data is synthetic, and no actual retention uplift is claimed. No customer messages are sent. Production use requires real-data validation, authentication and governance appropriate to the business, outcome maturity checks and intervention testing. Power BI import instructions and DAX are included; a native .pbix file is not.

The PDF retains the status at its original creation date. This file and the root README carry the current publication status.
