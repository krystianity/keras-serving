from __future__ import print_function

import numpy as np
import os
import shutil

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD

from keras import backend as K
K.set_learning_phase(0)

# training set

x = np.array([
    [0,0],
    [0,1],
    [1,0],
    [1,1]
])

y = np.array([
    [0],
    [1],
    [1],
    [0]
])

# build model

model = Sequential()
model.add(Dense(8, input_dim=2))
model.add(Activation("tanh"))
model.add(Dense(1))
model.add(Activation("sigmoid"))

sgd = SGD(lr=0.1)
model.compile(loss="binary_crossentropy", optimizer=sgd, metrics=["accuracy"])

# train model

model.fit(x, y, batch_size=1, epochs=1000)
print(model.predict_proba(x))

# write model to json file

if os.path.isdir("./result"):
    shutil.rmtree("./result")

os.makedirs("./result")

model_json = model.to_json()
with open("result/model.json", "w") as json_file: json_file.write(model_json)
model.save_weights("result/model.h5")
print("Saved model to disk")