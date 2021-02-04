# Train XGBoost built-in algorithm in SageMaker, inference with AWS Lambda

This examples illustrates how to target Direct Marketing with Amazon SageMaker XGBoost built-in algorithm, and inference with AWS Lambda.

You'll first train a SageMaker XGBoost built-in algorithm using the IPython notebook in [SageMaker Notebook instance](https://docs.aws.amazon.com/sagemaker/latest/dg/nbi.html). And then download the model to your computer, and build and deploy the Lambda function to perform the inference.

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

- notebooks - IPython notebook with the code to train a SageMaker XGBoost built-in algorithm.
- app - Code for the application's Lambda function.
- events - Invocation events that you can use to invoke the function.
- template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including Lambda functions. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.

## Train a SageMaker XGBoost built-in algorithm 
You'll be running the [Targeting Direct Marketing with Amazon SageMaker XGBoost, Inference with AWS Lambda](./notebooks/xgboost_direct_marketing_sagemaker_inference_with_lambda.ipynb) notebook to train a SageMaker XGBoost built-in algorithm.

You can run this notebook in [SageMaker Notebook instance](https://docs.aws.amazon.com/sagemaker/latest/dg/nbi.html)

This notebooks is identical to the original [Targeting Direct Marketing with Amazon SageMaker XGBoost](https://github.com/aws/amazon-sagemaker-examples/blob/master/introduction_to_applying_machine_learning/xgboost_direct_marketing/xgboost_direct_marketing_sagemaker.ipynb) notebook, except the fact that you'll deploy the model in Lambda function.

## Copy XGBoost model file and test data location in S3
Copy the XGBoost model and test data location in S3. This is required in order to be able to download the model to your computer, for the Lambda function to use, and to configure the Lambda test event.  

Copy model and test data location in S3 from the last two cells in the notebook

![Copy model and test data location in S3](../img/xgboost-built-in-algo-train-in-sagemaker-deploy-with-lambda-copy-outputs.png)

## Download XGBoost model file to your computer
Copy the XGBoost model file to `model` folder on your computer.

```bash
xgboost-built-in-algo-train-in-sagemaker-deploy-with-lambda$ aws s3 cp <MODEL_LOCATION_ON_S3> ./model/
```
Example:

```bash
xgboost-built-in-algo-train-in-sagemaker-deploy-with-lambda$ aws s3 cp s3://sagemaker-us-east-1-1234567890123/sagemaker/DEMO-xgboost-dm-lambda-inference/output/sagemaker-xgboost-2021-02-04-08-35-14-514/output/model.tar.gz ./model/
```

## Prepare test event for the Lambda
Update `bucket` and `prefix` values in [Lambda test event](./events/event.json) with the ones you copied form the IPyhton notebook.

This is the location of the test csv file for the Lambda to download from S3 and perform inference.

```json
{
  "bucket":"<REPLACE_WITH_YOUR_BUCKET_FROM_IPYTHON_NOTEBOOK>",
  "prefix":"<REPLACE_WITH_YOUR_PREFIX_FROM_IPYTHON_NOTEBOOK>",
  "file": "test.csv"
}
```

Example:

```json
{
  "bucket":"sagemaker-us-east-1-1234567890123",
  "prefix":"sagemaker/DEMO-xgboost-dm-lambda-inference/test/",
  "file": "test.csv"
}
```

## Deploy the sample application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

* SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

You may need the following for local testing.
* [Python 3 installed](https://www.python.org/downloads/)

To build and deploy your application for the first time, run the following in your shell:

```bash
sam build
sam deploy --guided
```

The first command will build a docker image from a Dockerfile and then copy the source of your application inside the Docker image. The second command will package and deploy your application to AWS, with a series of prompts:

* **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
* **AWS Region**: The AWS region you want to deploy your app to.
* **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modified IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

## Use the SAM CLI to build and test locally

Build your application with the `sam build` command.

```bash
xgboost-built-in-algo-train-in-sagemaker-deploy-with-lambda$ sam build
```

The SAM CLI builds a docker image from a Dockerfile and then installs dependencies defined in `requirements.txt` inside the docker image. The processed template file is saved in the `.aws-sam/build` folder.

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input that the function receives from the event source. Test events are included in the `events` folder in this project.

Run functions locally and invoke them with the `sam local invoke` command.

```bash
xgboost-built-in-algo-train-in-sagemaker-deploy-with-lambda$ sam local invoke XGBoostDMInferenceFunction --event events/event.json
```

## Testing your Lambda function in the Cloud

1. In the [Lambda Console](https://console.aws.amazon.com/lambda/), select Configure test events from the Test events dropdown.
2. For Event Name, enter InferenceTestEvent.
3. Copy the event JSON from [here](./events/event.json) and paste in the dialog box.
4. Choose _**Create**_.

![Configure test event](../img/xgboost_direct_marketing_configure_test_event.png)

After saving, you see InferenceTestEvent in the Test list. Now choose _**Test**_.

You see the Lambda function inference result, log output, and duration:

![Lambda execution result](../img/xgboost_direct_marketing_execution_result.png)

## Fetch, tail, and filter Lambda function logs

To simplify troubleshooting, SAM CLI has a command called `sam logs`. `sam logs` lets you fetch logs generated by your deployed Lambda function from the command line. In addition to printing the logs on the terminal, this command has several nifty features to help you quickly find the bug.

`NOTE`: This command works for all AWS Lambda functions; not just the ones you deploy using SAM.

```bash
xgboost-built-in-algo-train-in-sagemaker-deploy-with-lambda$ sam logs -n XGBoostDMInferenceFunction --stack-name xgboost-built-in-algo-train-in-sagemaker-deploy-with-lambda --tail
```

You can find more information and examples about filtering Lambda function logs in the [SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html).

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name xgboost-built-in-algo-train-in-sagemaker-deploy-with-lambda
```

## Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.

