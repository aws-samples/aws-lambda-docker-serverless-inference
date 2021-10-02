import sys
import os
import json
import joblib
import xgboost as xgb
import pandas as pd

loaded_model = joblib.load('./bc-xgboost-model')

def handler(event, context):
    print('Received event: ' + json.dumps(event, indent=2))
    
    payload_df = pd.json_normalize([event])
    result = loaded_model.predict(payload_df)
    
    print("Returning: {}".format(result[0]))
    return(json.dumps({"result": result[0]}))


