-- Historical outcomes only. One unique customer per snapshot in this demo.
SELECT snapshot_date, COUNT(*) AS customers, SUM(churn_next_30d) AS churned,
 AVG(churn_next_30d) AS churn_rate FROM historical_customers GROUP BY snapshot_date;
SELECT contract, COUNT(*) AS customers, AVG(churn_next_30d) AS churn_rate,
 AVG(monthly_charge) AS mean_monthly_charge_inr FROM historical_customers GROUP BY contract;
SELECT risk_band, COUNT(*) AS customers, AVG(churn_probability) AS mean_risk,
 SUM(monthly_charge) AS known_monthly_charges_inr, SUM(monthly_charge IS NULL) AS missing_charges
 FROM customer_scores GROUP BY risk_band;
SELECT customer_id, churn_probability, suggested_action, priority_rank
 FROM customer_scores WHERE contact_recommended=1 ORDER BY priority_rank LIMIT 100;
