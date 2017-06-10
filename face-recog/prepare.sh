#!/usr/bin/env bash
sudo apt install build-essential cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev python-tk
pip install pandas --user
pip install opencv-python --user
pip install statistics --user
pip install matplotlib --user
pip install pillow --user #required for pil (as scipy from numpy might not deliver..)