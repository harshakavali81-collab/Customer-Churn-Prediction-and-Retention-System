# Browser demo

This is a dependency-free static companion to the Python project. It uses the same fitted Logistic Regression parameters and preprocessing. Open through an HTTP server, not a file URL.

From the project root:
```
python -m http.server 8000 --directory browser-demo/dist
```
Then open http://localhost:8000.

To refresh the model export and compare predictions:
```
python -m src.export_browser --output browser-demo/dist
cd browser-demo
node test-parity.mjs
```

`core.mjs` implements scoring, CSV parsing and CSV output. `app.mjs` implements the visible UI. `data.json` and `sample_customers.csv` contain synthetic demonstration data. `parity.json` contains the Python reference outputs used by the test. These files have no real customer records.

Features: contract filtering, capacity-limited outreach, CSV upload and download, single-customer scoring, model evaluation and PDF/documentation links. No messages are sent, and uploads are not persisted.

Validation: JavaScript syntax, CSV/error cases and 1,103 Python/browser parity cases passed. A supported browser preview was unavailable in this environment, so visual browser QA and browser WebMCP registration testing were not performed. Optional WebMCP registration is feature-detected; normal UI behavior does not require it.
