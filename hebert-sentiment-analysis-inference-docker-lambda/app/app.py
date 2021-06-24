from transformers import pipeline
import json


sentiment_analysis = pipeline(
    "sentiment-analysis",
    model="./model",
    tokenizer="./model",
    return_all_scores = True
)

def handler(event, context):
    print('Received event: ' + json.dumps(event, indent=2))
    hebrew_text = event['hebrew_text']

    result = sentiment_analysis(hebrew_text)

    print('result: {}'.format(result))

    return json.dumps(result)
