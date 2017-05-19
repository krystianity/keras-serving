"use strict";

const express = require("express");
const bodyParser = require("body-parser");
const predict = require("./predict.js");

const app = express();

app.use(bodyParser.json());

app.get("/admin/healthcheck", (req, res) => {
    res.status(200).end("alive");
});

app.post("/predict", (req, res) => {

    if(!req.body || !req.body.inputs || !Array.isArray(req.body.inputs)){
        return res.status(400).json({error: "request body missing inputs array field."});
    }

    const inputs = req.body.inputs;
    predict(inputs, (error, outputs) => {

       if(error){
           return res.status(500).json({error});
       }

       res.status(200).json({outputs});
    });
});

app.listen(8080, () => {
    console.log("listening @ http://localhost:8080");
});