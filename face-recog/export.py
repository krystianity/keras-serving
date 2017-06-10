from __future__ import print_function
from keras import backend as K
from keras.models import load_model

from tensorflow.python.saved_model import builder as saved_model_builder
from tensorflow.python.saved_model import tag_constants, signature_constants
from tensorflow.python.saved_model.signature_def_utils_impl import build_signature_def, predict_signature_def

import shutil
import os

# loading models

emotion_model_path = './face-recog/trained_models/simple_CNN.530-0.65.hdf5'
gender_model_path = './face-recog/trained_models/simple_CNN.81-0.96.hdf5'

emotion_model = load_model(emotion_model_path)
gender_model = load_model(gender_model_path)

# prepare export dir

if os.path.isdir("./export"):
    shutil.rmtree("./export")

export_path_emotion = "export/main_model/1"
export_path_gender = "export/main_model/2"

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

signature_emotion = predict_signature_def(inputs={"inputs": emotion_model.input}, outputs={"output": emotion_model.output})
signature_gender = predict_signature_def(inputs={"inputs": gender_model.input}, outputs={"output": gender_model.output})

with K.get_session() as sess:
    builder_emotion.add_meta_graph_and_variables(sess=sess, tags=[tag_constants.SERVING], signature_def_map={'predict': signature_emotion})
    builder_emotion.save()
    builder_gender.add_meta_graph_and_variables(sess=sess, tags=[tag_constants.SERVING], signature_def_map={'predict': signature_gender})
    builder_gender.save()