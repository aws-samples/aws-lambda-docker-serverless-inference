package com.example;

import ai.djl.ModelException;
import ai.djl.inference.Predictor;
import ai.djl.modality.Classifications;
import ai.djl.modality.cv.Image;
import ai.djl.modality.cv.ImageFactory;
import ai.djl.repository.zoo.Criteria;
import ai.djl.repository.zoo.ModelZoo;
import ai.djl.repository.zoo.ZooModel;
import ai.djl.translate.TranslateException;
import ai.djl.util.Utils;
import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.LambdaLogger;
import com.amazonaws.services.lambda.runtime.RequestStreamHandler;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.nio.charset.StandardCharsets;

/**
 * Handler for requests to Lambda function.
 */
public class App implements RequestStreamHandler {

    private static final Gson GSON = new GsonBuilder().setPrettyPrinting().create();

    static {
        // DJL saves model and native libraries in cache folder.
        // In AWS-Lambda only /tmp folder is writable.
        System.setProperty("DJL_CACHE_DIR", "/tmp/djl_cache");
    }

    public void handleRequest(InputStream is, OutputStream os, Context context) throws IOException {
        LambdaLogger logger = context.getLogger();
        String input = Utils.toString(is);

        Request request = GSON.fromJson(input, Request.class);
        String inputImageUrl = request.getInputImageUrl();
        logger.log("inputImageUrl: " + inputImageUrl);

        try {

            Criteria<Image, Classifications> criteria = Criteria.builder()
                    .setTypes(Image.class, Classifications.class)
                    .optEngine("TFLite")
                    .optFilter("dataset", "aiyDish")
                    .build();
            ZooModel<Image, Classifications> model = ModelZoo.loadModel(criteria);

            Predictor<Image, Classifications> predictor = model.newPredictor();

            Image image = ImageFactory.getInstance().fromUrl(inputImageUrl);

            Classifications classifications = predictor.predict(image);

            logger.log("Classifications: " + classifications);
            os.write(GSON.toJson(classifications.best()).getBytes(StandardCharsets.UTF_8));

    } catch (RuntimeException | ModelException | TranslateException e) {
            logger.log("Failed handle input: " + input);
            logger.log(e.toString());
            String msg = "{\"status\": \"invoke failed: " + e.toString() + "\"}";
            os.write(msg.getBytes(StandardCharsets.UTF_8));
        }
    }
}
