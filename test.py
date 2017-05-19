from __future__ import print_function

from keras.optimizers import SGD
from keras.models import model_from_json
import numpy as np

# read model from file

json_file = open("result/model.json", "r")
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

# load weights into model
loaded_model.load_weights("result/model.h5")

sgd = SGD(lr=0.1)
loaded_model.compile(loss="binary_crossentropy", optimizer=sgd, metrics=["accuracy"])

print("Loaded model from disk")

# test

"""
test_x = np.array([
    [0,0],
    [0,1],
    [1,0],
    [1,1]
])
"""

test_x = np.array([[0,1]])

classes = loaded_model.predict(test_x, batch_size=1)
print("Result:", classes)