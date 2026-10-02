"""Export the fitted model for equivalent browser scoring."""
from pathlib import Path
import json,joblib,pandas as pd,numpy as np
from src.core import ROOT,NUM,CAT,prepare

def export(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    b=joblib.load(ROOT/'models/churn_model.joblib');pipe=b['model'];pre=pipe.named_steps['prepare'];model=pipe.named_steps['model']
    if b['model_name']!='logistic':raise ValueError('Browser export supports the selected logistic model only.')
    num=pre.named_transformers_['num'];cat=pre.named_transformers_['cat']
    payload={'numeric':NUM,'categorical':CAT,'medians':num.named_steps['impute'].statistics_.tolist(),'means':num.named_steps['scale'].mean_.tolist(),'scales':num.named_steps['scale'].scale_.tolist(),'modes':cat.named_steps['impute'].statistics_.tolist(),'categories':[x.tolist() for x in cat.named_steps['encode'].categories_],'coefficients':model.coef_[0].tolist(),'intercept':float(model.intercept_[0]),'threshold':b['threshold']}
    (output/'model.json').write_text(json.dumps(payload,allow_nan=False))
    current=pd.read_csv(ROOT/'data/current_customers.csv')
    hist=pd.read_csv(ROOT/'data/customers_clean.csv');hist=hist[hist.snapshot_date<'2025-11-01']
    data={'customers':json.loads(current.to_json(orient='records')),'metrics':json.loads((ROOT/'reports/metrics.json').read_text()),'comparison':json.loads(pd.read_csv(ROOT/'reports/model_comparison_validation.csv').to_json(orient='records')),'importance':json.loads(pd.read_csv(ROOT/'reports/feature_importance.csv').to_json(orient='records')),'historical':json.loads(hist.groupby('snapshot_date').agg(customers=('customer_id','size'),churn_rate=('churn_next_30d','mean')).reset_index().to_json(orient='records'))}
    (output/'data.json').write_text(json.dumps(data,allow_nan=False))
    edge=current.head(3).copy();edge.customer_id=['EDGE0','EDGE1','EDGE2'];edge.usage_previous=0;edge.monthly_charge=np.nan;edge.payment_method=np.nan
    checks=pd.concat([current,edge],ignore_index=True);expected=pipe.predict_proba(prepare(checks)[NUM+CAT])[:,1]
    tests={'rows':json.loads(checks.to_json(orient='records')),'expected':expected.tolist()}
    (output/'parity.json').write_text(json.dumps(tests,allow_nan=False))
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--output',default='browser-demo');a=p.parse_args();export(a.output)
