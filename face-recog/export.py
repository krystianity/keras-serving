from __future__ import print_function
from keras import backend as K
from keras.models import load_model
from keras.models import Sequential

from tensorflow.python.saved_model import builder as saved_model_builder
from tensorflow.python.saved_model import tag_constants, signature_constants
from tensorflow.python.saved_model.signature_def_utils_impl import build_signature_def, predict_signature_def

import tensorflow as tf
import shutil
import os

# loading models

emotion_model_path = './face-recog/trained_models/simple_CNN.530-0.65.hdf5'
gender_model_path = './face-recog/trained_models/simple_CNN.81-0.96.hdf5'

emotion_model = load_model(emotion_model_path)
gender_model = load_model(gender_model_path)

# reset learning phase
print(K.learning_phase())
K.set_learning_phase(0)
print(K.learning_phase())

emotion_config = emotion_model.get_config()
emotion_weights = emotion_model.get_weights()

emotion_model = Sequential.from_config(emotion_config)
emotion_model.set_weights(emotion_weights)

gender_config = gender_model.get_config()
gender_weights = gender_model.get_weights()

gender_model = Sequential.from_config(gender_config)
gender_model.set_weights(gender_weights)

# prepare export dir

if os.path.isdir("./export"):
    shutil.rmtree("./export")

export_path_emotion = "export/emotion_model/1"
export_path_gender = "export/gender_model/1"

# export models

builder_emotion = saved_model_builder.SavedModelBuilder(export_path_emotion)
builder_gender = saved_model_builder.SavedModelBuilder(export_path_gender)

print("- - -")
print(emotion_model.input)
print(emotion_model.output)
print("- - -")
print(gender_model.input)
print(gender_model.output)
print("- - -")

signature_emotion = predict_signature_def(inputs={"inputs": emotion_model.input}, outputs={"outputs": emotion_model.output})
signature_gender = predict_signature_def(inputs={"inputs": gender_model.input}, outputs={"outputs": gender_model.output})

with K.get_session() as sess:
    builder_emotion.add_meta_graph_and_variables(sess=sess, tags=[tag_constants.SERVING], signature_def_map={"predict": signature_emotion})
    builder_emotion.save()
    builder_gender.add_meta_graph_and_variables(sess=sess, tags=[tag_constants.SERVING], signature_def_map={"predict": signature_gender})
    builder_gender.save()