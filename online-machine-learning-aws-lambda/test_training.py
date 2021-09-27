from sklearn import datasets
import json
import requests

url = 'https://ofkwobdov5.execute-api.eu-central-1.amazonaws.com/Prod/training/'
headers = {'Content-Type': "application/json", 'Accept': "application/json"}

X, y = datasets.make_regression(
    n_samples=500,
    n_features=1,
    n_informative=1,
    n_targets=1,
    bias=20,
    noise=30
)

data = {
    "data": {
        "X": X.tolist(),
        "y": y.tolist()
    }
}

res = requests.post(url, json=json.dumps(data), headers=headers)

print(res)