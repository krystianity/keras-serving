"use strict";

const request = require("request");
const fs = require("fs");
const path = require("path");
const PNG = require("pngjs2").PNG;

function prepareInputs(input) {
    return input / 255.0;
}

function loadImageAsArray(filePath) {
    const faceData = fs.readFileSync(filePath); //should do this async in a prod environment
    const facePng = PNG.sync.read(faceData);
    const buffer = facePng.data;
    const flattened = []; //read image content into 48x48 array (only access first value r,g,b,a)
    for (let i = 0; i < buffer.length; i = i + 4) {
        flattened.push(prepareInputs(buffer[i]));
    }
    return flattened;
}

function makeRequest(imageData, endpoint = "/predict-emotion--and-gender") {
    return new Promise((resolve, reject) => {

        const options = {
            method: "POST",
            url: `http://localhost:8080${endpoint}`,
            headers: {
                "content-type": "application/json"
            },
            body: JSON.stringify({
                inputs: imageData
            })
        };

        request(options, (error, response, body) => {

            if (error) {
                return reject(error);
            }

            resolve(JSON.parse(body));
        });
    });
}


const args = process.argv[2];

if (!args) {
    return console.error("Please enter a path to an image face png file; e.g. ./../images/cutouts/4.png");
}

const faceFilePath = path.isAbsolute(args) ? args : path.join(__dirname, args);
console.log("Reading from path: " + faceFilePath);

const image = loadImageAsArray(faceFilePath);
console.log("Loaded image with size: " + image.length);

console.log("Making request to CNN GRPC wrapper.");
makeRequest(image)
    .then(res => console.log(JSON.stringify(res, null, 2)))
    .catch(error => console.error(error));