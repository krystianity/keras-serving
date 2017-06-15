# keras-serving

keras->tensorflow+grpc+docker=>nodejs :whale::fire:

- example of bringing a keras model to production using tensorflow serving
- using custom XOR model with tensor.proto dimensions example
- building & training of the model works with python2.7 on the workstation
- exported model is served via grpc in a C++ server using a Docker-Container
- a nodejs server wraps the grpc api for a simple http POST endpoint
- also ships an advanced multi-model face (emotion, gender) detection example `/face-recog`
- and and advanced google bigquery (as dataaset) example `/bigquery`

# Overview

* XOR Setup below
* [Face-Recog Setup](face-recog/)
* [BigQuery Setup](bigquery/)


# Workflow (Unix - testen on Ubuntu 16.04 64bit)

## You will need

```
python
pip
docker (docker-compose)
```

## 1. Install Requirements

```
./prepare.sh
# installs python dependencies via pip
# builds the docker image for tensorflow_serving (takes a while ~ 30 minutes)
# image size ~ 3.5 GB
```
checkout [build troubleshoot](build.md) if you are having trouble

## 2. Build, Train and Serialise Keras Model

```
python train.py
# results will be in (/result)
```

## 3. Load and export Model as Tensorflow Graph

```
python export.py
# results will be in (/export)
```

## 4. Build & Run Containers via docker-compose

```
./start-servers.sh
# ./stop-servers.sh
```

## 5. Test API via curl

```
curl -X POST \
  http://localhost:8080/predict-xor \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -d '{"inputs": [0,1]}'
```
