import unittest,json
import pandas as pd
import numpy as np
import joblib
from src.core import ROOT,prepare,score
from src.monitor import monitor
class ProjectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=pd.read_csv(ROOT/'data/current_customers.csv');cls.bundle=joblib.load(ROOT/'models/churn_model.joblib')
    def test_disjoint_splits(self):
        sets=[set(pd.read_csv(ROOT/f'reports/{s}_ids.csv').customer_id) for s in ['train','validation','test']]
        self.assertFalse(sets[0]&sets[1] or sets[0]&sets[2] or sets[1]&sets[2])
    def test_scores_and_target_exclusion(self):
        a=score(self.data,self.bundle);b=score(self.data.assign(churn_next_30d=1),self.bundle)
        np.testing.assert_allclose(a.churn_probability,b.churn_probability)
        self.assertTrue(a.churn_probability.between(0,1).all())
        self.assertEqual(len(a),len(self.data))
    def test_duplicate_ids_rejected(self):
        with self.assertRaises(ValueError):prepare(pd.concat([self.data,self.data.iloc[:1]]))
    def test_bad_numeric_rejected(self):
        d=self.data.copy();d.loc[0,'tenure_months']=-1
        with self.assertRaises(ValueError):prepare(d)
    def test_missing_schema_rejected(self):
        with self.assertRaises(ValueError):prepare(self.data.drop(columns='contract'))
    def test_zero_usage_and_missing_values(self):
        d=self.data.head(3).copy();d['usage_previous']=0;d['monthly_charge']=np.nan
        self.assertTrue(score(d,self.bundle).churn_probability.notna().all())
    def test_monitoring(self):
        result=monitor(self.data);json.dumps(result,allow_nan=False)
        self.assertEqual(result['rows'],1100)
    def test_validation_capacity(self):
        d=pd.read_csv(ROOT/'data/customers_clean.csv');v=d[d.snapshot_date=='2025-07-01']
        self.assertLessEqual(score(v,self.bundle).contact_recommended.mean(),.2)
    def test_app_pages(self):
        from streamlit.testing.v1 import AppTest
        app=AppTest.from_file(str(ROOT/'app.py')).run(timeout=30)
        self.assertEqual(len(app.exception),0)
        for page in ['Score customers','Model evaluation']:
            app.sidebar.radio[0].set_value(page).run(timeout=30)
            self.assertEqual(len(app.exception),0)
if __name__=='__main__':unittest.main()
