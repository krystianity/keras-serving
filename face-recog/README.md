# keras-serving face-recog (emotion and gender detection)

## Info

* models.py, utils.py and test.py are taken (and adjusted) from [oarriaga](https://github.com/oarriaga/face_classification)
* I am using the pre-trained models from oarriage, which he trained on the `fer2013.bib` [dataset](https://github.com/oarriaga/face_classification/tree/master/datasets/fer2013)
* Image face-classification is done by opencv's [haarcascade](https://github.com/opencv/opencv/tree/05b15943d6a42c99e5f921b7dbaa8323f3c042c6/data/haarcascades)
* oarriaga's project is under MIT License

## 1. Install Requirements

NOTICE: call these from the project root, not from inside the ./face-recog directory

```
./face-recog/prepare.sh
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
./start-dual-servers.sh
# ./stop-dual-servers.sh
```

## 4. Test API via client

* the client loads an image from whatever path (relative/absolute) you pass as first argument

```
cd ./face-recog/client
yarn (npm install -g yarn, in case you do not have it installed already)
yarn start ./../images/cutouts/4.png
# make sure to start the servers first
```

## 5. Generate and Test on your own images

```
cd ./face-recog/
python face-exporter.py ./images/chris_1.jpg 
# makes a gray cutout in 48x48 pixel of a face in the image
cd client
yarn start ./../images/face-exports/gray_0.png
```