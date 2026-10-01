# Data dictionary and provenance
Source: deterministic NumPy simulator in `src/pipeline.py`, seed 42. Units and relationships are invented for a subscription service demonstration. Not an external or company dataset.

| Field | Type / unit | Meaning |
|---|---|---|
| customer_id | string | Unique artificial identifier; excluded from model |
| snapshot_date | ISO date | Point-in-time observation; excluded from model |
| tenure_months | nonnegative number | Subscription age at snapshot |
| monthly_charge | INR/month | Current recurring charge; missing values allowed |
| usage_previous | nonnegative usage units | Usage during days -60 to -31 |
| usage_current | nonnegative usage units | Usage during days -30 to -1 |
| support_tickets | count | Tickets in preceding 30 days |
| failed_payments | count | Payment failures in preceding 30 days |
| contract | monthly / annual | Contract at snapshot |
| payment_method | automatic / manual | Payment arrangement at snapshot |
| churn_next_30d | 0/1 | Cancellation during next 30 days; target only |
| usage_change | decimal ratio | (current - previous) / previous; missing when denominator zero |

Missing model inputs are imputed inside the fitted pipeline; missing raw monetary values remain missing in exports to avoid fabricating revenue. Identifiers must be unique, numeric inputs finite and nonnegative, and categories valid. All uploaded columns outside the explicit feature list are excluded from the model. The scoring interface accepts the original fields and computes usage_change itself.

Output probability estimates are not guarantees. contact_recommended uses the validation cutoff; priority_rank orders descending risk with stable ties. Known charges aggregated over flagged customers are revenue exposure, not projected losses or saved revenue.
