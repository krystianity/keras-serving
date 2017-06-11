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

const flattened = [];
let x = 0;
let y = 0;
for (let i = 0; i < buffer.length; i = i + 4) {

    if (x !== 0 && x % 48 === 0) {
        y++;
        x = 0;
    }

    matrix[x][y] = buffer[i] / 255.0; //prepare inputs
    flattened.push(matrix[x][y]);
    x++;
}

console.log(flattened);
console.log(flattened.length);
console.log(48 * 48);

/*
the numpy gray_face array looks like this:
[[[[ 0.87843137]
   [ 0.8627451 ]
   [ 0.85882353]
   ..., 
   [ 0.86666667]
   [ 0.87843137]
   [ 0.90980392]]

  [[ 0.82745098]
   [ 0.83921569]
   [ 0.84705882]
   ..., 
   [ 0.87058824]
   [ 0.86666667]
   [ 0.8627451 ]]

  [[ 0.81176471]
   [ 0.80784314]
   [ 0.79607843]
   ..., 
*/

const options = {
    method: "POST",
    url: "http://localhost:8080/predict-face",
    headers: {
        "content-type": "application/json"
    },
    body: JSON.stringify({
        inputs: flattened
    })
};

request(options, (error, response, body) => {

    if (error) {
        return console.error(error);
    }

    console.log(error, response.statusCode, body);
});