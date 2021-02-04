import json
import pickle as pkl

import boto3
import numpy as np
import pandas as pd
import xgboost as xgb

s3 = boto3.client('s3')
model = pkl.load(open('xgboost-model', 'rb'))

def handler(event, context):
    print('Received event: ' + json.dumps(event, indent=2))

    destination = '/tmp/' + event["file"]
    s3.download_file(event["bucket"], event["prefix"] + event["file"], destination)
    data_csv = pd.read_csv(destination)

    dtest = xgb.DMatrix(data_csv.drop(['y_no', 'y_yes'], axis=1).values)
    predictions_local = model.predict(dtest)
    result = np.round(predictions_local).tolist()

    print("Returning: {}".format(result))
    return(json.dumps({"result": result}))


