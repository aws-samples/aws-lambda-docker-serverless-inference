package com.example;

import com.amazonaws.services.lambda.runtime.ClientContext;
import com.amazonaws.services.lambda.runtime.CognitoIdentity;
import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.LambdaLogger;

public class MockContext implements Context {

    @Override
    public String getAwsRequestId() {
        return "495b12a8-xmpl-4eca-8168-160484189f99";
    }

    @Override
    public String getLogGroupName() {
        return "/aws/lambda/my-function";
    }

    @Override
    public String getLogStreamName() {
        return "2020/02/26/[$LATEST]704f8dxmpla04097b9134246b8438f1a";
    }

    @Override
    public String getFunctionName() {
        return "my-function";
    }

    @Override
    public String getFunctionVersion() {
        return "$LATEST";
    }

    @Override
    public String getInvokedFunctionArn() {
        return "arn:aws:lambda:us-east-2:123456789012:function:my-function";
    }

    @Override
    public CognitoIdentity getIdentity() {
        return null;
    }

    @Override
    public ClientContext getClientContext() {
        return null;
    }

    @Override
    public int getRemainingTimeInMillis() {
        return 300000;
    }

    @Override
    public int getMemoryLimitInMB() {
        return 512;
    }

    @Override
    public LambdaLogger getLogger() {
        return new MockLogger();
    }
}