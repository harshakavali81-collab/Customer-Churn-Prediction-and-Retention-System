# Verification

- Full seeded data → training → scoring → SQL/report pipeline completed.
- Nine unittest checks passed, including all three Streamlit pages via AppTest, split isolation, target exclusion, invalid schema/IDs/numeric input, zero usage, monitoring serialization and validation outreach capacity.
- Notebook code cells executed successfully against the shipped data.
- Model performance chart visually checked.
- Dependency versions match the execution environment (Python 3.12).
- Docker build, Windows PowerShell upload script, hosted CI, public deployment and native Power BI rendering have not been executed.
- No real business retention uplift has been measured.

## Browser companion and hosted CI

- Original GitHub Actions run 36837646270 passed on Python 3.11.
- Browser scorer checked against Python on 1,103 records, including missing and zero-usage edge cases. Maximum absolute probability difference: 2.22e-16.
- CSV quoting, malformed input, duplicate IDs, invalid categories and negative-number validation passed.
- A supported browser preview was unavailable. Browser visual QA and optional WebMCP registration validation remain unperformed.
