from __future__ import print_function

import numpy as np
import keras

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import RMSprop
from keras.utils.data_utils import get_file
from keras.models import model_from_json

# download dataset from aws and load into numpy arrays

path="mnist.npz"
path = get_file(path, origin="https://s3.amazonaws.com/img-datasets/mnist.npz")
f = np.load(path)
x_train = f["x_train"]
y_train = f["y_train"]
x_test = f["x_test"]
y_test = f["y_test"]
f.close()

batch_size = 128
num_classes = 10
epochs = 20

# shuffle and split data between train and test sets

x_train = x_train.reshape(60000, 784)
x_test = x_test.reshape(10000, 784)
x_train = x_train.astype("float32")
x_test = x_test.astype("float32")
x_train /= 255
x_test /= 255
print(x_train.shape[0], "train samples")
print(x_test.shape[0], "test samples")

# convert class vectors to binary class matrices

y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

# build model

model = Sequential()

model.add(Dense(512, activation="relu", input_shape=(784,)))
model.add(Dropout(0.2))
model.add(Dense(512, activation="relu"))
model.add(Dropout(0.2))
model.add(Dense(10, activation="softmax"))

model.summary()

model.compile(loss="categorical_crossentropy",
              optimizer=RMSprop(),
              metrics=["accuracy"])

# train model

history = model.fit(x_train, y_train,
                    batch_size=batch_size,
                    epochs=epochs,
                    verbose=1,
                    validation_data=(x_test, y_test))

# test model

score = model.evaluate(x_test, y_test, verbose=0)

print("Test loss:", score[0])
print("Test accuracy:", score[1])

# write model to json file

model_json = model.to_json()
with open("result/model.json", "w") as json_file: json_file.write(model_json)
model.save_weights("result/model.h5")
print("Saved model to disk")

# read model from file

json_file = open("result/model.json", "r")
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

# load weights into model
loaded_model.load_weights("result/model.h5")

loaded_model.compile(loss="categorical_crossentropy",
                     optimizer=RMSprop(),
                     metrics=["accuracy"])

print("Loaded model from disk")

# test loaded model again

score2 = loaded_model.evaluate(x_test, y_test, verbose=0)
print("(Loaded)Test loss:", score[0])
print("(Loaded)Test accuracy:", score[1])

# predict with loaded model

classes = loaded_model.predict(x_test, batch_size=128)
print("Prediction result:", classes)