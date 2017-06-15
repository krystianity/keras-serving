"use strict";

const grpc = require("grpc");

const SERVER_PORT = 9000;
const XOR_CONSTR = `model-server:${SERVER_PORT}`;
const EMOTION_CONSTR = `emotion-server:${SERVER_PORT}`;
const GENDER_CONSTR = `gender-server:${SERVER_PORT}`;

const PROTO_PATH = __dirname + "/protos/prediction_service.proto";
const TensorflowServing = grpc.load(PROTO_PATH).tensorflow.serving;

/*
    this should actually be split in a 
    generic client/predict class
*/

const xorClient = new TensorflowServing.PredictionService(
    XOR_CONSTR, grpc.credentials.createInsecure()
);

const emotionClient = new TensorflowServing.PredictionService(
    EMOTION_CONSTR, grpc.credentials.createInsecure()
);

const genderClient = new TensorflowServing.PredictionService(
    GENDER_CONSTR, grpc.credentials.createInsecure()
);

function getXORModelMsg(vals) {
    return {
        model_spec: { name: "main_model", signature_name: "predict", version: 1 },
        inputs: {
            inputs: {
                dtype: "DT_FLOAT",
                tensor_shape: {
                    dim: [{
                            size: 1
                        },
                        {
                            size: 2
                        }
                    ]
                },
                float_val: vals
            }
        }
    };
}

function getEmotionModelMsg(vals) {
    return {
        model_spec: { name: "emotion_model", signature_name: "predict", version: 1 },
        inputs: {
            inputs: {
                dtype: "DT_FLOAT",
                tensor_shape: {
                    dim: [{
                            size: 1
                        },
                        {
                            size: 48
                        },
                        {
                            size: 48
                        },
                        {
                            size: 1
                        }
                    ],
                    unknown_rank: false
                },
                float_val: vals
            }
        }
    };
}

function getGenderModelMsg(vals) {
    return {
        model_spec: { name: "gender_model", signature_name: "predict", version: 1 },
        inputs: {
            inputs: {
                dtype: "DT_FLOAT",
                tensor_shape: {
                    dim: [{
                            size: 1
                        },
                        {
                            size: 48
                        },
                        {
                            size: 48
                        },
                        {
                            size: 3
                        }
                    ],
                    unknown_rank: false
                },
                float_val: vals
            }
        }
    };
}

function predictXOR(array, callback) {
    xorClient.predict(getXORModelMsg(array), (error, response) => {

        if (error) {
            return callback(error);
        }

        callback(null, response.outputs.outputs.float_val);
    });
}

function predictEmotion(array, callback) {
    emotionClient.predict(getEmotionModelMsg(array), (error, response) => {

        if (error) {
            return callback(error);
        }

        callback(null, response.outputs.outputs.float_val);
    });
}

function predictGender(array, callback) {
    genderClient.predict(getGenderModelMsg(array), (error, response) => {

        if (error) {
            return callback(error);
        }

        callback(null, response.outputs.outputs.float_val);
    });
}

module.exports = {
    predictXOR,
    predictEmotion,
    predictGender
};