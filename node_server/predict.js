"use strict";

const grpc = require("grpc");

const CONSTR = "model-server:9000";
const PROTO_PATH = __dirname + "/protos/prediction_service.proto";

const TensorflowServing = grpc.load(PROTO_PATH).tensorflow.serving;

const client = new TensorflowServing.PredictionService(
    CONSTR, grpc.credentials.createInsecure()
);

function getFloatMatrixMsg(vals, dimX = 1, dimY = 2) {
    return {
        model_spec: { name: "main_model", signature_name: "predict", version: 1 },
        inputs: {
            inputs: {
                dtype: "DT_FLOAT",
                tensor_shape: {
                    dim: [{ //defines dimensions of tensor
                            size: dimX
                        },
                        {
                            size: dimY
                        }
                    ]
                },
                float_val: vals
            }
        }
    };
}

function getBufferMsg(bufferArray) {
    return {
        model_spec: { name: "main_model", signature_name: "predict", version: 1 },
        inputs: {
            inputs: {
                dtype: "DT_STRING",
                tensor_shape: {
                    dim: {
                        size: bufferArray.length
                    }
                },
                string_val: bufferArray
            }
        }
    };
}

function predict(matrix, callback) {
    client.predict(getFloatMatrixMsg(matrix), (error, response) => {

        if (error) {
            return callback(error);
        }

        callback(null, response.outputs.outputs.float_val);
    });
}

function predictFace(matrix, callback) {
    client.predict(getBufferMsg(matrix), (error, response) => {

        if (error) {
            return callback(error);
        }

        callback(null, response.outputs.outputs.float_val);
    });
}

module.exports = {
    predict,
    predictFace
};