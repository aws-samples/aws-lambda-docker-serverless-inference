import json
import boto3
import os
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
import tempfile
import joblib

s3 = boto3.client('s3')
logger = Logger(service="inference")

BUCKET_NAME = os.environ['BUCKET_NAME']
model_name = 'model.joblib'


def _download_model_from_s3(model_key):
    with tempfile.TemporaryFile() as fp:
        s3.download_fileobj(BUCKET_NAME, model_key, fp)
        fp.seek(0)
        model = joblib.load(fp)
    return model


# Lambda handler code
@logger.inject_lambda_context
def lambda_handler(event, _):
    event = APIGatewayProxyEvent(event)
    logger.info(event.__dict__)
    # parse input event
    data = event.get('body')
    data = json.loads(data)
    data = data.get("data")
    # download current model from s3
    regr = _download_model_from_s3(model_name)
    # make prediction
    pred = regr.predict(data)
    # log prediction
    logger.info({
        "data": data,
        "prediction": pred,
    })

    return {
        'statusCode': 200,
        'body': json.dumps(
            {
                "prediction": json.dumps(pred.tolist()),
            }
        )
    }
