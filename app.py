from pathlib import Path
import json
import joblib
import pandas as pd
import streamlit as st
from src.core import ROOT, score
st.set_page_config(page_title='Customer Retention Studio',page_icon='📊',layout='wide')
st.title('Customer Retention Studio')
st.caption('Synthetic portfolio demonstration • 30-day cancellation risk • Charges in INR')
@st.cache_resource
def load_model(): return joblib.load(ROOT/'models/churn_model.joblib')
if not (ROOT/'models/churn_model.joblib').exists():
    st.error('Run python -m src.pipeline first.');st.stop()
bundle=load_model()
page=st.sidebar.radio('Workspace',['Overview','Score customers','Model evaluation'])
if page=='Overview':
    d=pd.read_csv(ROOT/'data/customer_scores.csv')
    contracts=st.sidebar.multiselect('Contract',sorted(d.contract.unique()),default=sorted(d.contract.unique()))
    d=d[d.contract.isin(contracts)]
    a,b,c=st.columns(3);a.metric('Current customers',len(d));b.metric('Flagged for contact',int(d.contact_recommended.sum()));c.metric('Mean predicted risk',f'{d.churn_probability.mean():.1%}' if len(d) else '—')
    st.subheader('Risk distribution');st.bar_chart(d.risk_band.value_counts().reindex(['Low','Medium','High'],fill_value=0))
    st.subheader('Prioritized retention queue')
    capacity=st.slider('Outreach capacity',10,500,100,10)
    queue=d[d.contact_recommended].sort_values('priority_rank').head(capacity)
    st.dataframe(queue,hide_index=True,width='stretch')
    st.download_button('Download outreach queue',queue.to_csv(index=False),'retention_queue.csv','text/csv')
    st.caption('Suggested actions follow observable billing, support and usage rules. They are not causal model explanations. Risk bands use 30% and 60%; the contact threshold is selected separately on validation data.')
elif page=='Score customers':
    st.write('Upload the same schema as the sample. No outcome column is required. Maximum 20,000 rows.')
    sample=pd.read_csv(ROOT/'data/current_customers.csv').head(10)
    st.download_button('Download sample CSV',sample.to_csv(index=False),'sample_customers.csv','text/csv')
    upload=st.file_uploader('Customer CSV',type='csv')
    if upload:
        try:
            data=pd.read_csv(upload)
            if len(data)>20000: raise ValueError('Limit is 20,000 rows.')
            scored=score(data,bundle)
            st.dataframe(scored,hide_index=True)
            st.download_button('Download predictions',scored.to_csv(index=False),'predictions.csv','text/csv')
        except (ValueError,KeyError,TypeError) as e: st.error(str(e))
else:
    m=json.loads((ROOT/'reports/metrics.json').read_text())
    st.write('Selected model:',m['model'])
    a,b,c=st.columns(3);a.metric('Holdout ROC-AUC',f"{m['roc_auc']:.3f}");b.metric('Average precision',f"{m['average_precision']:.3f}");c.metric('Recall',f"{m['recall']:.1%}")
    st.image(str(ROOT/'reports/model_performance.png'))
    st.dataframe(pd.read_csv(ROOT/'reports/model_comparison_validation.csv'),hide_index=True)
    st.subheader('Global feature importance on validation data')
    st.bar_chart(pd.read_csv(ROOT/'reports/feature_importance.csv').set_index('feature')['mean_ap_decrease'])
    st.warning('Synthetic evaluation only. Validate on real, consented historical data before business use.')
