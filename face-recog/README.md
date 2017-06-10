# keras-serving face-recog (emotion and gender detection)

## Info

* models.py, utils.py and test.py are taken (and adjusted) from [oarriaga](https://github.com/oarriaga/face_classification)
* I am using the pre-trained models from oarriage, which he trained on the `fer2013.bib` [dataset](https://github.com/oarriaga/face_classification/tree/master/datasets/fer2013)
* Image face-classification is done by opencv's [haarcascade](https://github.com/opencv/opencv/tree/05b15943d6a42c99e5f921b7dbaa8323f3c042c6/data/haarcascades)

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
cd /face-recog/client
npm install
npm start # make sure to start the servers first
```