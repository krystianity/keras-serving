"use strict";

const request = require("request");
const fs = require("fs");
const path = require("path");
const PNG = require("pngjs2").PNG;

const faceFile = path.join(__dirname, "./../images/cutouts/5.png");
const faceData = fs.readFileSync(faceFile);
const facePng = PNG.sync.read(faceData);

const buffer = facePng.data;

const matrix = [];
for (let i = 0; i < 48; i++) {
    matrix.push([]);
}

let x = 0;
let y = 0;

for (let i = 0; i < buffer.length; i = i + 4) {

    if (x !== 0 && x % 48 === 0) {
        y++;
        x = 0;
    }

    matrix[x][y] = buffer[i];
    x++;
}

const options = {
    method: "POST",
    url: "http://localhost:8080/predict-face",
    headers: {
        "content-type": "application/json"
    },
    body: JSON.stringify({
        inputs: [faceData]
    })
};

request(options, (error, response, body) => {
    console.log(error, response.statusCode, body);
});