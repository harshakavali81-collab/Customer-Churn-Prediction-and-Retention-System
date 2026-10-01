# Power BI dashboard build
A native `.pbix` is not included; the working dashboard is Streamlit. This guide supplies a reproducible Power BI layout and measures.

1. Get Data → Text/CSV: import `data/customers_clean.csv` as `Historical`, filter snapshot_date before 2025-11-01 in Power Query. Import `data/customer_scores.csv` as `Scores`.
2. Set customer_id to Text, snapshot_date to Date, monetary/probability columns to Decimal and contact_recommended to True/False. Check CSV booleans convert correctly.
3. Keep these as separate cohort tables; do not join historical outcomes to different current customers.
4. Add the measures below. Format rate measures as percentages and monetary values as INR.
5. Page 1: historical customer count, churn rate, churn by contract, churn by snapshot date; contract and date slicers.
6. Page 2: current customers, flagged customers, known flagged MRR, missing-charge count, risk-band count chart and outreach table sorted by priority_rank; contract and risk-band slicers.
7. Label the file and pages “Synthetic demonstration”. Import validation comparison and test predictions on a third model-performance page if desired.

```dax
Historical Customers = COUNTROWS(Historical)
Churned Customers = SUM(Historical[churn_next_30d])
Churn Rate = DIVIDE([Churned Customers], [Historical Customers])
Current Customers = COUNTROWS(Scores)
Flagged Customers = CALCULATE(COUNTROWS(Scores), Scores[contact_recommended] = TRUE())
Mean Predicted Risk = AVERAGE(Scores[churn_probability])
Known Flagged MRR = CALCULATE(SUM(Scores[monthly_charge]), Scores[contact_recommended] = TRUE())
Flagged Missing Charges = CALCULATE(COUNTROWS(Scores), Scores[contact_recommended] = TRUE(), ISBLANK(Scores[monthly_charge]))
```
Known Flagged MRR is the sum of nonmissing charges among flagged customers, not loss or revenue saved. Always show its missing-charge count. Refresh CSV sources after running the pipeline and resolve file paths on your computer.
