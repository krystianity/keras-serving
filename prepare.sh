#!/usr/bin/env bash
pip install keras --user
pip install tensorflow --user
pip install h5py --user
docker build -t tf-model-server model_server