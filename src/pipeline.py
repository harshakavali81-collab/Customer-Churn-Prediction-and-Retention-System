"""Reproduce all synthetic data, model artifacts, reports and SQL outputs."""
import json, sqlite3, platform
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import joblib, sklearn
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import average_precision_score, roc_auc_score, precision_score, recall_score, f1_score, brier_score_loss, confusion_matrix, RocCurveDisplay, PrecisionRecallDisplay
from sklearn.inspection import permutation_importance
from src.core import ROOT,NUM,CAT,prepare,score

def generate(n=6600):
    rng = np.random.default_rng(42)
    d = pd.DataFrame({'customer_id':[f'C{i:05}' for i in range(n)],
        'snapshot_date':np.repeat(['2025-01-01','2025-03-01','2025-05-01','2025-07-01','2025-09-01','2025-11-01'],n//6),
        'tenure_months':rng.integers(1,73,n), 'monthly_charge':rng.uniform(199,2499,n).round(2),
        'usage_previous':rng.uniform(5,100,n).round(2), 'support_tickets':rng.poisson(1,n),
        'failed_payments':rng.binomial(2,.12,n), 'contract':rng.choice(['monthly','annual'],n,p=[.7,.3]),
        'payment_method':rng.choice(['automatic','manual'],n,p=[.6,.4])})
    change = np.clip(rng.normal(-.08,.35,n),-.95,1)
    d['usage_current'] = (d.usage_previous*(1+change)).round(2)
    logit = -2.5 + 1.0*(d.contract=='monthly') + .6*(d.payment_method=='manual') + .48*d.support_tickets + .85*d.failed_payments - .018*d.tenure_months - 2.5*change + .00022*d.monthly_charge
    d['churn_next_30d'] = rng.binomial(1,1/(1+np.exp(-logit)))
    for c in ['monthly_charge','usage_current','payment_method']:
        d.loc[rng.choice(n,66,replace=False),c] = np.nan
    return pd.concat([d,d.iloc[:20]],ignore_index=True)

def metrics(y,p,t):
    pred=p>=t
    return { 'roc_auc':float(roc_auc_score(y,p)), 'average_precision':float(average_precision_score(y,p)),
       'precision':float(precision_score(y,pred,zero_division=0)), 'recall':float(recall_score(y,pred)),
       'f1':float(f1_score(y,pred)), 'brier':float(brier_score_loss(y,p)), 'contact_rate':float(pred.mean()) }

def main():
    for folder in ['data','models','reports']: (ROOT/folder).mkdir(exist_ok=True)
    raw=generate(); raw.to_csv(ROOT/'data/customers_raw.csv',index=False)
    unique=raw.drop_duplicates('customer_id').copy(); d=prepare(unique)
    d.to_csv(ROOT/'data/customers_clean.csv',index=False)
    train=d[d.snapshot_date<='2025-05-01']; val=d[d.snapshot_date=='2025-07-01']; test=d[d.snapshot_date=='2025-09-01']; current=d[d.snapshot_date=='2025-11-01']
    current.drop(columns='churn_next_30d').to_csv(ROOT/'data/current_customers.csv',index=False)
    X=train[NUM+CAT]; y=train.churn_next_30d
    models={'baseline':DummyClassifier(strategy='prior'), 'logistic':LogisticRegression(max_iter=1000),
            'random_forest':RandomForestClassifier(n_estimators=160,min_samples_leaf=12,random_state=42,n_jobs=2),
            'gradient_boosting':HistGradientBoostingClassifier(max_iter=100,max_leaf_nodes=15,l2_regularization=5,random_state=42)}
    fitted={}; rows=[]
    for name, estimator in models.items():
        pre=ColumnTransformer([('num',Pipeline([('impute',SimpleImputer(strategy='median')),('scale',StandardScaler())]),NUM),
                               ('cat',Pipeline([('impute',SimpleImputer(strategy='most_frequent')),('encode',OneHotEncoder(handle_unknown='ignore',sparse_output=False))]),CAT)])
        pipe=Pipeline([('prepare',pre),('model',estimator)]).fit(X,y)
        p=pipe.predict_proba(val[NUM+CAT])[:,1]
        rows.append({'model':name,**metrics(val.churn_next_30d,p,.5)}); fitted[name]=pipe
    comparisons=pd.DataFrame(rows).sort_values('average_precision',ascending=False)
    comparisons.to_csv(ROOT/'reports/model_comparison_validation.csv',index=False)
    name=comparisons.iloc[0]['model']; model=fitted[name]
    vp=model.predict_proba(val[NUM+CAT])[:,1]
    # Policy: contact at most 20% of validation cohort. Strict cutoff handles ties.
    threshold=float(np.nextafter(np.sort(vp)[-int(.2*len(vp))-1],1.0))
    bundle={'model':model,'threshold':threshold,'model_name':name,'sklearn_version':sklearn.__version__}
    joblib.dump(bundle,ROOT/'models/churn_model.joblib')
    tp=model.predict_proba(test[NUM+CAT])[:,1]; result=metrics(test.churn_next_30d,tp,threshold)
    result.update(model=name,threshold=threshold,test_rows=len(test),test_churn_rate=float(test.churn_next_30d.mean()),confusion_matrix=confusion_matrix(test.churn_next_30d,tp>=threshold).tolist())
    result['precision_lift']=result['precision']/result['test_churn_rate']
    (ROOT/'reports/metrics.json').write_text(json.dumps(result,indent=2))
    for label,part in [('train',train),('validation',val),('test',test)]:
        part[['customer_id','snapshot_date']].assign(split=label).to_csv(ROOT/f'reports/{label}_ids.csv',index=False)
    scored=score(current,bundle); scored.to_csv(ROOT/'data/customer_scores.csv',index=False)
    scored[scored.contact_recommended].to_csv(ROOT/'data/retention_outreach.csv',index=False)
    pd.DataFrame({'customer_id':test.customer_id,'actual':test.churn_next_30d,'probability':tp}).to_csv(ROOT/'reports/test_predictions.csv',index=False)
    importance=permutation_importance(model,val[NUM+CAT],val.churn_next_30d,scoring='average_precision',n_repeats=5,random_state=42,n_jobs=2)
    pd.DataFrame({'feature':NUM+CAT,'mean_ap_decrease':importance.importances_mean,'std':importance.importances_std}).sort_values('mean_ap_decrease',ascending=False).to_csv(ROOT/'reports/feature_importance.csv',index=False)
    fig,ax=plt.subplots(1,2,figsize=(11,4)); RocCurveDisplay.from_predictions(test.churn_next_30d,tp,ax=ax[0]); PrecisionRecallDisplay.from_predictions(test.churn_next_30d,tp,ax=ax[1]); fig.suptitle('Synthetic holdout performance'); fig.tight_layout(); fig.savefig(ROOT/'reports/model_performance.png',dpi=150);plt.close(fig)
    hist=d[d.snapshot_date<'2025-11-01']
    fig,ax=plt.subplots(1,2,figsize=(11,4)); hist.groupby('contract').churn_next_30d.mean().plot.bar(ax=ax[0],color=['#0f766e','#6366f1']); ax[0].set_title('Observed churn by contract');ax[0].set_ylabel('Churn fraction');ax[0].tick_params(axis='x',rotation=0);scored.churn_probability.plot.hist(ax=ax[1],bins=20,color='#6366f1');ax[1].set_title('Current cohort risk scores');fig.tight_layout();fig.savefig(ROOT/'reports/eda.png',dpi=150);plt.close(fig)
    with sqlite3.connect(ROOT/'data/churn.db') as con:
        hist.to_sql('historical_customers',con,if_exists='replace',index=False)
        scored.to_sql('customer_scores',con,if_exists='replace',index=False)
        queries=(ROOT/'sql/analysis.sql').read_text().split(';')
        for i,q in enumerate(queries):
            if q.strip(): pd.read_sql_query(q,con).to_csv(ROOT/f'reports/sql_result_{i+1}.csv',index=False)
    manifest={'seed':42,'synthetic':True,'raw_rows':len(raw),'duplicates_removed':len(raw)-len(d),'unique_rows':len(d),'train':len(train),'validation':len(val),'test':len(test),'current':len(current),'python':platform.python_version(),'sklearn':sklearn.__version__,'missing_by_column':unique.isna().sum().to_dict()}
    (ROOT/'reports/data_quality.json').write_text(json.dumps(manifest,indent=2))
    report=f'''# Results — synthetic demonstration\n\nSelected model: {name}. Training: {len(train)}; validation: {len(val)}; holdout: {len(test)}; current scoring: {len(current)} customers.\n\nHoldout ROC-AUC: {result['roc_auc']:.3f}. Average precision: {result['average_precision']:.3f} versus prevalence {result['test_churn_rate']:.3f}.\nPrecision: {result['precision']:.1%}; recall: {result['recall']:.1%}; F1: {result['f1']:.3f}; Brier score: {result['brier']:.3f}.\nValidation-selected threshold: {threshold:.4f}. Holdout contact rate: {result['contact_rate']:.1%}. Precision lift: {result['precision_lift']:.2f}x.\n\nCurrent cohort: {int(scored.contact_recommended.sum())} flagged. Outreach is ranked by risk; an operational team should cap the list to its capacity.\n\n## Interpretation\nThese metrics measure recovery of the simulator's patterns, not real customer behavior. Contract, usage, support and payment features were deliberately used to generate outcomes. Retention actions are transparent business rules, not causal explanations or proven interventions.\n\n## Next experiment\nRandomly assign eligible customers to intervention and control. Predefine 30-day retention, treatment cost, gross margin and complaint guardrails. Estimate treatment-control retention difference with uncertainty. Do not claim revenue saved from predicted risk alone.\n'''
    (ROOT/'reports/RESULTS.md').write_text(report)
    print(json.dumps(result,indent=2))
if __name__=='__main__': main()
