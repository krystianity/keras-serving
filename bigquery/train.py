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

# load data from big-query

bq = bigquery.Client()

project = ""
bq_table = "analytics.access_log"
of_date = "2017-05-29"

bq_query = """
    SELECT user_agent, ip, received_at, url  
    FROM `{}.{}`
    WHERE _PARTITIONTIME = TIMESTAMP("{}") 
    LIMIT 40000;
""".format(project, bq_table, of_date)

query_results = bq.run_sync_query(bq_query)
query_results.use_legacy_sql = False

print("bq running query.")
print(float(sh.awk(sh.ps('u','-p',os.getpid()),'{sum=sum+$6}; END {print sum/1024}')))
query_results.run()

dataset_x = []
dataset_y = []
page_token = None

print("bq query run.")

while True:
    rows, total_rows, page_token = query_results.fetch_data(
        max_results=8000,
        page_token=page_token)

    print("bq fetched 8k rows.")

    for row in rows:
        (user_agent, ip, received_at, url) = row
        dataset_x.append([user_agent, ip, url])
        dataset_y.append([received_at])

    if not page_token:
        break

print("bq data fetched.")
print(float(sh.awk(sh.ps('u','-p',os.getpid()),'{sum=sum+$6}; END {print sum/1024}')))

# training set

dataset_x = np.array(dataset_x)
dataset_y = np.array(dataset_y)

print(dataset_x.size)
print(dataset_y.size)

print(dataset_x[0])
print(dataset_y[0])

print(float(sh.awk(sh.ps('u','-p',os.getpid()),'{sum=sum+$6}; END {print sum/1024}')))

# build model

model = Sequential()
model.add(Dense(8, input_dim=3))
model.add(Activation("tanh"))
model.add(Dense(1))
model.add(Activation("sigmoid"))

sgd = SGD(lr=0.1)
model.compile(loss="binary_crossentropy", optimizer=sgd, metrics=["accuracy"])

# train model

model.fit(dataset_x, dataset_y, batch_size=1, epochs=1000)
print(model.predict_proba(x))

# write model to json file

if os.path.isdir("./result"):
    shutil.rmtree("./result")

os.makedirs("./result")

model_json = model.to_json()
with open("./result/model.json", "w") as json_file: json_file.write(model_json)
model.save_weights("./result/model.h5")
print("Saved model to disk")