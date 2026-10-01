from pathlib import Path
import numpy as np
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
NUM = ['tenure_months','monthly_charge','usage_previous','usage_current','support_tickets','failed_payments','usage_change']
CAT = ['contract','payment_method']
RAW = NUM[:-1] + CAT

def prepare(df):
    df = df.copy()
    missing = set(RAW + ['customer_id']) - set(df.columns)
    if missing: raise ValueError(f'Missing columns: {sorted(missing)}')
    if df.empty: raise ValueError('Upload at least one customer.')
    if df.customer_id.isna().any() or df.customer_id.duplicated().any():
        raise ValueError('Customer IDs must be present and unique.')
    for col in RAW:
        if col in CAT:
            df[col] = df[col].astype('string').str.strip().str.lower().replace('', pd.NA).astype(object)
            df[col] = df[col].where(pd.notna(df[col]), np.nan)
        else:
            df[col] = pd.to_numeric(df[col], errors='raise')
            if np.isinf(df[col]).any() or (df[col].dropna() < 0).any():
                raise ValueError(f'{col} must contain finite nonnegative numbers or blanks.')
    for col, allowed in {'contract':{'monthly','annual'}, 'payment_method':{'automatic','manual'}}.items():
        if not set(df[col].dropna()).issubset(allowed): raise ValueError(f'{col}: allowed values {sorted(allowed)}')
    df['usage_change'] = (df.usage_current - df.usage_previous) / df.usage_previous.replace(0, np.nan)
    return df

def actions(df):
    return np.select([df.failed_payments.fillna(0)>0, df.support_tickets.fillna(0)>=3, df.usage_change.fillna(0)<-.25],
                     ['Billing assistance','Resolve support issues','Offer onboarding session'], default='Review needs with customer')

def score(df, bundle):
    d = prepare(df)
    out = d[['customer_id','contract','monthly_charge']].copy()
    out['churn_probability'] = bundle['model'].predict_proba(d[NUM+CAT])[:,1]
    out['contact_recommended'] = out.churn_probability >= bundle['threshold']
    out['risk_band'] = pd.cut(out.churn_probability,[-1,.3,.6,1],labels=['Low','Medium','High'])
    out['suggested_action'] = actions(d)
    out.loc[~out.contact_recommended,'suggested_action'] = 'Regular engagement'
    out['priority_rank'] = out.churn_probability.rank(method='first',ascending=False).astype(int)
    return out.sort_values('priority_rank')
