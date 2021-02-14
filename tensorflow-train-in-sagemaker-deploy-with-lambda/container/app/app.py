import json

import boto3
import numpy as np
import tensorflow as tf

s3 = boto3.client('s3')

# Loading model
model_path = './000000001/'
loaded_model = tf.saved_model.load(model_path)
infer = loaded_model.signatures['serving_default']

def handler(event, context):
    print('Received event: ' + json.dumps(event, indent=2))

    destination = '/tmp/' + event["file"]
    s3.download_file(event["bucket"], event["prefix"] + event["file"], destination)
    data = np.load(destination)

    predictions = infer(tf.constant(data))['dense_1']
    print('predictions: {}'.format(predictions))

    result=[]
    for element in predictions:
        prediction = np.argmax(element)
        result.append(int(prediction))

    print('Returning result: {}'.format(result))

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }