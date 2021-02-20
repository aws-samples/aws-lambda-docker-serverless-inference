import joblib
import json
from sklearn.datasets import load_iris

loaded_model = joblib.load('./iris_classifier_knn.joblib')
iris = load_iris()

def handler(event, context):
    print('Received event: ' + json.dumps(event, indent=2))

    predictions = loaded_model.predict(event["data"])
    predictions_species = [iris.target_names[p] for p in predictions]

    print("Returning: {}".format(predictions_species))
    return(json.dumps({"predictions": predictions_species}))


