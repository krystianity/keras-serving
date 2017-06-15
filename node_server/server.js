"use strict";

/*
    please note:
    the code of this server has not been optimized,
    you might want to adjust a few things before
    running this in production.
*/

const express = require("express");
const bodyParser = require("body-parser");
const async = require("async");

const {
    predictXOR,
    predictEmotion,
    predictGender
} = require("./predict.js");

const EMOTION_MAPPER = {
    0: "angry",
    1: "disgust",
    2: "sad",
    3: "happy",
    4: "sad",
    5: "surprise",
    6: "neutral"
};

const GENDER_MAPPER = {
    0: "woman",
    1: "man"
};

function maxArgIndex(arr) {
    return Math.round(arr.indexOf(Math.max(...arr)));
}

const app = express();

app.use(bodyParser.json());

app.get("/admin/healthcheck", (req, res) => {
    res.status(200).end("alive");
});

app.post("/predict-xor", (req, res) => {

    if (!req.body || !req.body.inputs || !Array.isArray(req.body.inputs)) {
        return res.status(400).json({ error: "request body missing inputs array field." });
    }

    const inputs = req.body.inputs;
    predictXOR(inputs, (error, outputs) => {

        if (error) {
            console.error(error);
            return res.status(500).json({ error });
        }

        console.log("xor-prediction successfull.");
        res.status(200).json({ outputs });
    });
});

app.post("/predict-emotion", (req, res) => {

    if (!req.body || !req.body.inputs || !Array.isArray(req.body.inputs)) {
        return res.status(400).json({ error: "request body missing inputs array field." });
    }

    const inputs = req.body.inputs;
    predictEmotion(inputs, (error, outputs) => {

        if (error) {
            console.error(error);
            return res.status(500).json({ error });
        }

        console.log("face-prediction successfull.");

        let identifiedEmotion = null;
        try {
            identifiedEmotion = EMOTION_MAPPER[maxArgIndex(outputs)];
        } catch (error) {
            res.status(500).json({ error });
        }

        res.status(200).json({ outputs, identifiedEmotion });
    });
});

app.post("/predict-gender", (req, res) => {

    if (!req.body || !req.body.inputs || !Array.isArray(req.body.inputs)) {
        return res.status(400).json({ error: "request body missing inputs array field." });
    }

    const inputs = req.body.inputs;
    predictGender(inputs, (error, outputs) => {

        if (error) {
            console.error(error);
            return res.status(500).json({ error });
        }

        console.log("gender-prediction successfull.");

        let identifiedGender = null;
        try {
            identifiedGender = GENDER_MAPPER[maxArgIndex(outputs)];
        } catch (error) {
            res.status(500).json({ error });
        }

        res.status(200).json({ outputs, identifiedGender });
    });
});

app.post("/predict-emotion--and-gender", (req, res) => {

    if (!req.body || !req.body.inputs || !Array.isArray(req.body.inputs)) {
        return res.status(400).json({ error: "request body missing inputs array field." });
    }

    const inputs = req.body.inputs;

    const calls = [
        callback => {
            predictGender(inputs, (error, outputs) => {

                if (error) {
                    return callback(error);
                }

                callback(null, {
                    gender: GENDER_MAPPER[maxArgIndex(outputs)],
                    outputs
                });
            });
        },
        callback => {
            predictEmotion(inputs, (error, outputs) => {

                if (error) {
                    return callback(error);
                }

                callback(null, {
                    emotion: EMOTION_MAPPER[maxArgIndex(outputs)],
                    outputs
                });
            });
        }
    ];

    //call both cnn grpc services in parallel
    async.parallel(calls, (error, results) => {

        if (error) {
            console.error(error);
            return res.status(500).json({ error });
        }

        console.log("gender-and-emotion-prediction successfull.");
        res.status(200).json({ results });
    });
});

app.listen(8080, () => {
    console.log("listening @ http://localhost:8080");
});