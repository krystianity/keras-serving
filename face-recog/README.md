# keras-serving face-recog (emotion and gender detection)

## 1. Install Requirements

```
./prepare.sh # ./face-recog/prepare.sh
# installs python dependencies via pip
# also make sure you already have built the docker-image for the XOR project /README.md#1
```

## 2. Re-import and export Model as Tensorflow Graph

```
python face-recog/export.py # make sure to run from project root folder
# results will be in (/export)
```

## 3. Build & Run Containers via docker-compose

```
./start-servers.sh
# ./stop-servers.sh
```

## 4. Test API via client

* the client loads an image from /face-recog/images/cutouts/

```
curl -X POST \
  http://localhost:8080/predict \
  -H 'cache-control: no-cache' \
  -H 'content-type: application/json' \
  -d '{"inputs": [0,1]}'
```
