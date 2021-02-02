# Pay as you go inference with AWS Lambda (Docker image)

This repository contains resources to help you deploy Lambda functions based on Python and Java Docker Images. 

The applications deployed illustrate how to perform inference using Lambda Function.

## Overview

AWS Lambda is one of the most cost effective service that lets you run code without provisioning or managing servers. 

It offers many advantages when working with serverless infrastructure. When you break down the logic of your machine learning service into a single Lambda function for a single request, things become much simpler and easy to scale. 

You can forget all about the resource handling needed for the parallel requests coming into your model. 

**If your usage is sparse and tolerable to a higher latency, Lambda is a great choice among various solutions.**

### Repository Structure

The repository contains the following resources:

- **XGBoost resources:**  

  - [**Serverless XGBoost Model Serving**](xgboost-inference-docker-lambda):  This examples illustrates how to serve XGBoost model on Lambda Function to predict breast cancer.
  
- **Deep Java Library (DJL) resources:**  

  - [**Serverless Object Detection Model Serving with Deep Java Library (DJL)**](djl-object-detection-inference-docker-lambda):  This example illustrates how to serve TensorFlow Object Detection model on Lambda Function using [Deep Java Library (DJL)](http://djl.ai)..   



## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

