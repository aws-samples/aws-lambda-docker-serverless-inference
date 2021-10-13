import json
import boto3
import os
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

import tempfile
import joblib

s3 = boto3.client('s3')
logger = Logger(service="training")

BUCKET_NAME = os.environ['BUCKET_NAME']
model_name = 'model.joblib'


def _upload_model_to_s3(model, model_key):
    with tempfile.TemporaryFile() as fp:
        joblib.dump(model, fp)
        fp.seek(0)
        s3.upload_fileobj(fp, BUCKET_NAME, model_key)


def _train_regression_model(X_train, y_train):
    # Create linear regression object
    regr = linear_model.LinearRegression()
    # Train the model using the training sets
    regr.fit(X_train, y_train)
    return regr


def _test_model(model, X_test, y_test):
    # Make predictions using the testing set
    y_pred = model.predict(X_test)
    # calculate quality coefficients
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return mse, r2


def _parse_input(event):
    # extract input data from event
    data = event.get('body')
    d = json.loads(data)
    print('data', d.get("data"))
    logger.info(d)
    X = d["data"]['X']
    y = d["data"]['y']
    # Split the data into training/testing sets
    X_train = X[:-20]
    X_test = X[-20:]
    # Split the targets into training/testing sets
    y_train = y[:-20]
    y_test = y[-20:]
    return X_train, X_test, y_train, y_test


# Lambda handler code
@logger.inject_lambda_context
def lambda_handler(event, _):
    event = APIGatewayProxyEvent(event)
    print(f'bucketname: {BUCKET_NAME}')
    logger.info(event.__dict__)
    # parse input event and split dataset
    X_train, X_test, y_train, y_test = _parse_input(event)
    # train regression model
    regr = _train_regression_model(X_train, y_train)
    # test model
    mse, r2 = _test_model(regr, X_test, y_test)
    logger.info({
        "message": "model training successful",
        'mean_squared_error': mse,
        'r_squared': r2
    })

    # save trained model to s3
    _upload_model_to_s3(regr, model_name)
    logger.info({
        "message": "model saved to s3",
        'bucket_name': BUCKET_NAME,
        'model_name': model_name
    })

    return {
        'statusCode': 200,
        'body': json.dumps(
            {
                'training': 'success',
                'mean_squared_error': mse,
                'r_squared': r2
            }
        )
    }
