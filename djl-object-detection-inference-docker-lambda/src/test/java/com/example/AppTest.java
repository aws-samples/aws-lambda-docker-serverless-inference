package com.example;

import ai.djl.modality.Classifications;
import com.amazonaws.services.lambda.runtime.Context;
import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.lang.reflect.Type;
import java.nio.charset.StandardCharsets;
import java.util.List;
import org.testng.Assert;
import org.testng.annotations.Test;

public class AppTest {

  @Test
  public void invokeTest() throws IOException {
    Context context = new MockContext();
    App app = new App();

    Request request = new Request();
    request.setInputImageUrl("https://djl-ai.s3.amazonaws.com/resources/images/kitten.jpg");
    Gson gson = new Gson();
    byte[] buf = gson.toJson(request).getBytes(StandardCharsets.UTF_8);

    InputStream is = new ByteArrayInputStream(buf);
    ByteArrayOutputStream os = new ByteArrayOutputStream();
    app.handleRequest(is, os, context);
    String result = os.toString(StandardCharsets.UTF_8.name());

    Type type = new TypeToken<List<Classifications.Classification>>() {}.getType();
    List<Classifications.Classification> list = gson.fromJson(result, type);
    Assert.assertNotNull(list);
    Assert.assertEquals(list.get(0).getClassName(), "n02123045 tabby, tabby cat");
  }
}
