import fasttext
import json

loaded_model = fasttext.load_model('./model.bin')


def handler(event, context):
    print('Received event: ' + json.dumps(event, indent=2))

    prediction = loaded_model.predict(event["text"])

    print("Returning: {}".format(prediction))
    return(json.dumps({"prediction": prediction[0][0]}))


