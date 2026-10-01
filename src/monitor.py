import argparse, json
import numpy as np
import pandas as pd
import joblib
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss
from src.core import ROOT,NUM,CAT,prepare,score

def monitor(batch, labels=None):
    current=prepare(batch)
    ref=pd.read_csv(ROOT/'data/customers_clean.csv')
    ref=ref[ref.snapshot_date<='2025-05-01']
    checks=[]
    for col in NUM+CAT:
        delta=float(current[col].isna().mean()-ref[col].isna().mean())
        check={'feature':col,'missing_rate_change':delta,'review':abs(delta)>.1}
        if col in NUM:
            scale=ref[col].std()
            shift=abs(current[col].mean()-ref[col].mean())/scale if scale>0 else 0
            check['mean_shift_in_training_std']=float(shift) if pd.notna(shift) else None
            check['review']=bool(check['review'] or pd.isna(shift) or shift>.5)
        checks.append(check)
    result={'rows':len(current),'checks':checks,'outcome_metrics':None,'note':'Heuristic drift checks; not proof of model decay. Labels must be mature.'}
    if labels is not None:
        if not {'customer_id','actual'}.issubset(labels): raise ValueError('Labels need customer_id and actual')
        if labels.customer_id.duplicated().any() or labels.actual.isna().any() or not set(labels.actual).issubset({0,1}):raise ValueError('Labels must be unique binary outcomes')
        scored=score(current,joblib.load(ROOT/'models/churn_model.joblib'))
        merged=scored.merge(labels,on='customer_id',validate='one_to_one')
        if len(merged)!=len(current): raise ValueError('Labels must cover the entire input cohort')
        if merged.actual.nunique()<2:raise ValueError('Both outcome classes required for ROC-AUC')
        result['outcome_metrics']={'roc_auc':roc_auc_score(merged.actual,merged.churn_probability),'average_precision':average_precision_score(merged.actual,merged.churn_probability),'brier':brier_score_loss(merged.actual,merged.churn_probability)}
    return result
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--input',required=True);parser.add_argument('--labels');parser.add_argument('--output',default='reports/monitoring.json');args=parser.parse_args()
    result=monitor(pd.read_csv(args.input),pd.read_csv(args.labels) if args.labels else None)
    from pathlib import Path
    Path(args.output).write_text(json.dumps(result,indent=2,allow_nan=False));print(args.output)
