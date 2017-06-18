from __future__ import print_function

from keras import backend as K

from tensorflow.python.saved_model import builder as saved_model_builder
from tensorflow.python.saved_model import tag_constants, signature_constants
from tensorflow.python.saved_model.signature_def_utils_impl import build_signature_def, predict_signature_def

from keras.optimizers import SGD
from keras.models import model_from_json
#from keras.models import Model

import shutil
import os
import numpy as np
import tensorflow as tf

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

if os.path.isdir("./export"):
    shutil.rmtree("./export")

# test
classes = loaded_model.predict(np.array([[0,1]]), batch_size=1)
print("Test:", classes)


# prepare model for export

"""
K.set_learning_phase(0)

config = loaded_model.get_config()
weights = loaded_model.get_weights()

model = Model.from_config(config)
model.set_weights(weights)
"""

model = loaded_model

# export model

export_path = "export/main_model/1"

builder = saved_model_builder.SavedModelBuilder(export_path)

print(model.input)
print(model.output)

signature = predict_signature_def(inputs={"inputs": model.input},
                                  outputs={"outputs": model.output})

with K.get_session() as sess:
    builder.add_meta_graph_and_variables(sess=sess,
                                         tags=[tag_constants.SERVING],
                                         signature_def_map={'predict': signature})
    builder.save()