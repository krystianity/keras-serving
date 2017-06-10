"use strict";

/*
    please note:
    the code of this server has not been optimized
    you might want to adjust a few things before
    running this in production.
*/

const express = require("express");
const bodyParser = require("body-parser");
const { predict, predictFace } = require("./predict.js");

const app = express();

app.use(bodyParser.json());

app.get("/admin/healthcheck", (req, res) => {
    res.status(200).end("alive");
});

app.post("/predict", (req, res) => {

    if (!req.body || !req.body.inputs || !Array.isArray(req.body.inputs)) {
        return res.status(400).json({ error: "request body missing inputs array field." });
    }

    const inputs = req.body.inputs;
    predict(inputs, (error, outputs) => {

        if (error) {
            console.error(error);
            return res.status(500).json({ error });
        }

        console.log("prediction successfull.");
        res.status(200).json({ outputs });
    });
});

app.post("/predict-face", (req, res) => {

    if (!req.body || !req.body.inputs || !Array.isArray(req.body.inputs)) {
        return res.status(400).json({ error: "request body missing inputs array field." });
    }

    const inputs = req.body.inputs.map(input => new Buffer(input, "binary"));

    predictFace(inputs, (error, outputs) => {

        if (error) {
            console.error(error);
            return res.status(500).json({ error });
        }

        console.log("face-prediction successfull.");
        res.status(200).json({ outputs });
    });
});

app.listen(8080, () => {
    console.log("listening @ http://localhost:8080");
});