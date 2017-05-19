"use strict";

const grpc = require("grpc");

const CONSTR = "model-server:9000";
const PROTO_PATH = __dirname + "/protos/prediction_service.proto";

const TensorflowServing = grpc.load(PROTO_PATH).tensorflow.serving;

const client = new TensorflowServing.PredictionService(
    CONSTR, grpc.credentials.createInsecure()
);

function getMsg(vals){
    return {
        model_spec: { name: "main_model", signature_name: "predict", version: 1 },
        inputs: {
            inputs: {
                dtype: "DT_FLOAT",
                tensor_shape: {
                    dim: [{ //defines dimensions of tensor
                        size: 1
                    },
                    {
                        size: 2
                    }]
                },
                float_val: vals
            }
        }
    };
}

function predict(matrix, callback){
    client.predict(getMsg(matrix), (error, response) => {

        if(error){
            return callback(error);
        }

        callback(null, response.outputs.outputs.float_val);
    });
}

module.exports = predict;