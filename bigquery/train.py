from __future__ import print_function

import numpy as np
import os
import shutil
import sh

from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD

from google.cloud import bigquery

from keras import backend as K
K.set_learning_phase(0)

# def utils

def print_mem_usage():
    print(float(sh.awk(sh.ps('u','-p',os.getpid()),'{sum=sum+$6}; END {print sum/1024}')), "mb")
    return

# build & compile model

print("building & compiling model")

model = Sequential()
model.add(Dense(8, input_dim=3))
model.add(Activation("tanh"))
model.add(Dense(1))
model.add(Activation("sigmoid"))

sgd = SGD(lr=0.1)
model.compile(loss="binary_crossentropy", optimizer=sgd, metrics=["accuracy"])

# load data from big-query

bq = bigquery.Client()

project = ""
bq_table = "analytics.access_log"
of_date = "2017-05-29"
bq_limit = 120000

bq_query = """
    SELECT user_agent, ip, received_at, url  
    FROM `{}.{}`
    WHERE _PARTITIONTIME = TIMESTAMP("{}") 
    LIMIT {};
""".format(project, bq_table, of_date, bq_limit)

query_results = bq.run_sync_query(bq_query)
query_results.use_legacy_sql = False

print("bq running query.")
print_mem_usage()
query_results.run()

def prepare_x_dataset_row(row):
    (user_agent, ip, received_at, url) = row
    #dataset = [user_agent, ip, url]
    dataset = [0.1, 0.2, 0.3]
    return dataset

def prepare_y_dataset_row(row):
    (user_agent, ip, received_at, url) = row
    #dataset = [received_at]
    dataset = [0.4]
    return dataset

def handle_bq_data(rows):
    
    dataset_x = []
    dataset_y = []

    for row in rows:

        xrow = prepare_x_dataset_row(row)
        yrow = prepare_y_dataset_row(row)

        dataset_x.append(xrow)
        dataset_y.append(yrow)

    dataset_x = np.array(dataset_x)
    dataset_y = np.array(dataset_y)

    return (dataset_x, dataset_y)

def batch_train_model(datasets):
    (x,y) = datasets
    model.fit(x, y, batch_size=10, epochs=2)
    return

print("fetching bq data and training model.")
bq_count = 0
page_token = None
while True:
    rows, total_rows, page_token = query_results.fetch_data(
        max_results=4000,
        page_token=page_token)

    print("bq fetched ~4k rows.")
    datasets = handle_bq_data(rows)
    batch_train_model(datasets)
    print_mem_usage()
    bq_count = bq_count + len(rows)
    progress = bq_count * 100 / bq_limit 
    print(bq_count, "/", bq_limit, "=>", progress, "%")

    if not page_token:
        break

print("bq data fetched.")
print_mem_usage()

print("done")
#print(model.predict_proba(x))

# write model to json file

#if os.path.isdir("./result"):
#    shutil.rmtree("./result")

#os.makedirs("./result")

#model_json = model.to_json()
#with open("./result/model.json", "w") as json_file: json_file.write(model_json)
#model.save_weights("./result/model.h5")
#print("Saved model to disk")