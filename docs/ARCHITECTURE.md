# System architecture and workflow

## Offline model training

```mermaid
flowchart TD
    A[Seeded synthetic records] --> B[Validation and deduplication]
    B --> C[Usage change feature]
    C --> D[Chronological cohorts]
    D --> E[Training-only preprocessing]
    E --> F[Candidate models]
    F --> G[Validation selection and threshold]
    G --> H[Untouched holdout evaluation]
    G --> I[Fitted model artifact]
    H --> J[Reports and diagnostic plots]
    I --> K[Current customer scoring]
    K --> L[Ranked retention queue]
```

The target describes cancellation in the 30 days after a snapshot. All model inputs are observed before the snapshot. Each simulated customer occurs once. The two-month cohort spacing provides an outcome-maturity gap.

## Two interfaces, one trained model

```mermaid
flowchart TD
    A[Fitted Python model] --> B[Streamlit interface]
    A --> C[Export preprocessing and coefficients]
    C --> D[Browser scorer]
    E[Customer CSV] --> B
    E --> D
    B --> F[Predictions and outreach queue]
    D --> F
    G[Python reference predictions] --> H[Parity verification]
    D --> H
```

The browser export supports the selected Logistic Regression model. It includes training medians/modes, standardization values, category order, coefficients, intercept and contact threshold. Browser inference matches Python across 1,103 records to less than 1e-9 absolute probability error. Changing the selected estimator to a tree model requires a new browser implementation; export fails explicitly for unsupported models.

## Retention decision

```mermaid
flowchart TD
    A[Predicted probability] --> B{Contact cutoff met?}
    B -->|No| C[Regular engagement]
    B -->|Yes| D[Apply billing, support and usage rules]
    D --> E[Rank by churn probability]
    E --> F[Select top customers within capacity]
    F --> G[Human review]
    G --> H[Optional future controlled experiment]
```

The app does not send messages or contact customers. Risk ranking is not treatment-effect estimation. The action rules choose the first matching issue and must be tested before business impact is claimed.

## Files and reproduction

| Component | Entry point |
|---|---|
| Training and reporting | `python -m src.pipeline` |
| Streamlit dashboard | `python -m streamlit run app.py` |
| Model export | `python -m src.export_browser --output browser-demo/dist` |
| Browser parity tests | `cd browser-demo` then `node test-parity.mjs` |
| Browser local preview | `python -m http.server 8000 --directory browser-demo/dist` |
| Monitoring | `python -m src.monitor --input data/current_customers.csv` |

Open the local preview at `http://localhost:8000`. Do not double-click index.html, because browser module and JSON loading require an HTTP server.

The static demo processes user-supplied CSV files in browser memory. It does not upload them to a prediction backend or persist them after refresh. The Python project remains the source for training and monitoring.
