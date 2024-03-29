# Serverless scikit-learn training and inference

This project contains source code and supporting files for a serverless application for training and serving a Machine Learning model in [scikit-learn](https://scikit-learn.org/). The following image illustrates the application's architecture:

![Alt text](./img/architecture_diagram.png?raw=true "Title")

This example includes the following files and folders:

- app/lambda_inference/         - Code for the application's inference Lambda function.
- app/lambda_training/          - Code for the application's training Lambda function.
- app/*/app.py                  - Code for the application's Lambda function.
- app/*/Dockerfile              - The Dockerfile to build the container image.
- app/*/requirements.txt        - The pip requirements to be installed during the container build.
- template.yaml                 - A template that defines the application's AWS resources.
- events/inference_event.json   - A sample payload to test the inference Lambda function locally.
- events/train_event.json       - A sample payload to test the training Lambda function locally.
- env.json                      - Json file to add the bucket name of your deployed S3 model bucket for local testing of the Lambda functions.
- notebooks/test_notebook.ipynb - A Jupyter notebook to test the lambda function in the cloud by invoking them directly and through API Gateway.

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.

While this template does not use any auth, you will almost certainly want to use auth in order to productionize. Please follow [these instructions](https://github.com/aws/serverless-application-model/blob/master/versions/2016-10-31.md#function-auth-object) to set up auth with SAM.

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
* **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
* **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

You can find your API Gateway Endpoint URL in the output values displayed after deployment.

## Use the SAM CLI to build and test locally

Build your application with the `sam build` command.

```bash
online-ml$ sam build
```

The SAM CLI builds a docker image from a Dockerfile and then installs dependencies defined in `app/*/requirements.txt` inside the docker image. The processed template file is saved in the `.aws-sam/build` folder.

Test a single function by invoking it directly with a test event. An event is a JSON document that represents the input that the function receives from the event source. Test events are included in the `events` folder in this project.

In order to have your local lambda function access the correct S3 bucket, access the AWS console, go to `CloudFormation` under stacks click on `serverless-online-ml`, click on `Resources` and copy the `Physical ID` of your `ModelBucket`. 
Paste the physical ID in the `env.json` in the respective fields of the two lambda functions:

```json
{
  "TrainingFunction": {
    "BUCKET_NAME": "serverless-online-ml-modelbucket-xxxxxxxxxx" //Replace this string with your physical ID
  },
  "InferenceFunction": {
    "BUCKET_NAME": "serverless-online-ml-modelbucket-xxxxxxxxxx" //Replace this string with your physical ID
  }
}
```
Run functions locally and invoke them with the `sam local invoke` command.
```bash
online-ml$ sam local invoke TrainingFunction --event events/train_event.json --env-vars env.json
online-ml$ sam local invoke InferenceFunction --event events/inference_event.json --env-vars env.json
```

## Add a resource to your application
The application template uses AWS Serverless Application Model (AWS SAM) to define application resources. AWS SAM is an extension of AWS CloudFormation with a simpler syntax for configuring common serverless application resources such as functions, triggers, and APIs. For resources not included in [the SAM specification](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md), you can use standard [AWS CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html) resource types.

## Fetch, tail, and filter Lambda function logs

To simplify troubleshooting, SAM CLI has a command called `sam logs`. `sam logs` lets you fetch logs generated by your deployed Lambda function from the command line. In addition to printing the logs on the terminal, this command has several nifty features to help you quickly find the bug.

`NOTE`: This command works for all AWS Lambda functions; not just the ones you deploy using SAM.

```bash
online-ml$ sam logs -n InferenceFunction --stack-name online-ml --tail
```

You can find more information and examples about filtering Lambda function logs in the [SAM CLI Documentation](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-logging.html).

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name online-ml
```

## Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.

Next, you can use AWS Serverless Application Repository to deploy ready to use Apps that go beyond hello world samples and learn how authors developed their applications: [AWS Serverless Application Repository main page](https://aws.amazon.com/serverless/serverlessrepo/)
