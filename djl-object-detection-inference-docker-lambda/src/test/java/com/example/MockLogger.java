package com.example;

import com.amazonaws.services.lambda.runtime.LambdaLogger;
import java.nio.charset.StandardCharsets;

public class MockLogger implements LambdaLogger {

    @Override
    public void log(String message) {
        System.out.println(message);
    }

    @Override
    public void log(byte[] message) {
        System.out.println(new String(message, StandardCharsets.UTF_8));
    }
}