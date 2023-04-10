# %%
import tensorflow_hub as hub
import tensorflow_text as text
import tensorflow as tf
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt
from official.nlp import optimization
import pandas as pd
from keras import backend as K
import csv

from sklearn.metrics import classification_report
plt.style.use('ggplot')
# %%

df = pd.read_csv('assets/training_data.csv', delimiter='␟', quoting=3, usecols=["id", "tweet_content", "topic"])

df.head()

num_classes = len(df["topic"].value_counts())

df = df[df.topic.notnull()]

# %%
colors = plt.cm.Dark2(np.linspace(0, 1, num_classes))
iter_color = iter(colors)

df['topic'].value_counts().plot.barh(title="Topic (n, %)", 
                                                 ylabel="Topics",
                                                 color=colors,
                                                 figsize=(9,9))

for i, v in enumerate(df['topic'].value_counts()):
  c = next(iter_color)
  plt.text(v, i,
           " "+str(v)+", "+str(round(v*100/df.shape[0],2))+"%", 
           color=c, 
           va='center', 
           fontweight='bold')
  
# %%
print(np.where(df['topic'].isnull())[0])

# %%


df['Labels'] = df['topic'].map({'Health': 0,
                                    'Politics': 1,
                                    'Vaccines': 2,
                                    'News': 3,
                                    'Social': 4,
                                    'Lockdown': 5,
                                    'Masks': 6,
                                    'Unmarked': 7}).astype(int)

# drop unused column
df = df.drop(["topic"], axis=1)

df.head()

# %%
y = tf.keras.utils.to_categorical(df["Labels"].values, num_classes=num_classes)

x_train, x_test, y_train, y_test = train_test_split(df['tweet_content'], y, test_size=0.25)

x_train = np.asarray(x_train).astype('str')
y_train = np.asarray(y_train).astype('int32')

tf.cast(x_train, dtype=tf.string)
tf.cast(y_train, dtype=tf.int32)

x_test = np.asarray(x_train).astype('str')
y_test = np.asarray(y_train).astype('int32')

tf.cast(x_test, dtype=tf.string)
tf.cast(y_test, dtype=tf.int32)

# %%
preprocessor = hub.KerasLayer("https://tfhub.dev/tensorflow/bert_en_cased_preprocess/3")
encoder = hub.KerasLayer("https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-2_H-128_A-2/2")
# %%


def balanced_recall(y_true, y_pred):
    recall_by_class = 0
    for i in range(y_pred.shape[1]):
        y_pred_class = y_pred[:, i]
        y_true_class = y_true[:, i]
        true_positives = K.sum(K.round(K.clip(y_true_class * y_pred_class, 0, 1)))
        possible_positives = K.sum(K.round(K.clip(y_true_class, 0, 1)))
        recall = true_positives / (possible_positives + K.epsilon())
        recall_by_class = recall_by_class + recall
    return recall_by_class / y_pred.shape[1]

def balanced_precision(y_true, y_pred):
    precision_by_class = 0
    for i in range(y_pred.shape[1]):
        y_pred_class = y_pred[:, i]
        y_true_class = y_true[:, i]
        true_positives = K.sum(K.round(K.clip(y_true_class * y_pred_class, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred_class, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())
        precision_by_class = precision_by_class + precision
    return precision_by_class / y_pred.shape[1]

def balanced_f1_score(y_true, y_pred):
    precision = balanced_precision(y_true, y_pred)
    recall = balanced_recall(y_true, y_pred)
    return 2 * ((precision * recall) / (precision + recall + K.epsilon()))

i = tf.keras.layers.Input(shape=(), dtype=tf.string, name='text')
x = preprocessor(i)
x = encoder(x)
x = tf.keras.layers.Dropout(0.1, name="dropout")(x['pooled_output'])
x = tf.keras.layers.Dense(num_classes, activation='softmax', name="output")(x)

model = tf.keras.Model(i, x)


# %%

METRICS = [
      tf.keras.metrics.CategoricalAccuracy(name="accuracy"),
      balanced_recall,
      balanced_precision,
      balanced_f1_score
]

epochs = 40
steps_per_epoch = 2750

earlystop_callback = tf.keras.callbacks.EarlyStopping(monitor = "val_loss", 
                                                      patience = 3,
                                                      restore_best_weights = True)

model.compile(optimizer = "adam",
              loss = "categorical_crossentropy",
              metrics = METRICS)

model_fit = model.fit(x_train, 
                      y_train, 
                      epochs = epochs,
                      steps_per_epoch = steps_per_epoch,
                      validation_data = (x_test, y_test),
                      callbacks = [earlystop_callback]
                    )

# %%

x = list(range(1, epochs+1))
metric_list = list(model_fit.history.keys())
num_metrics = int(len(metric_list)/2)

fig, ax = plt.subplots(nrows=1, ncols=num_metrics, figsize=(30, 5))

for i in range(0, num_metrics):
  ax[i].plot(x, model_fit.history[metric_list[i]], marker="o", label=metric_list[i].replace("_", " "))
  ax[i].plot(x, model_fit.history[metric_list[i+num_metrics]], marker="o", label=metric_list[i+num_metrics].replace("_", " "))
  ax[i].set_xlabel("epochs",fontsize=14)
  ax[i].set_title(metric_list[i].replace("_", " "),fontsize=20)
  ax[i].legend(loc="lower left")
  
# %%
# Testing Model
def predict_class(data):
  '''predict class of input text
  Args:
    - data (list of strings)
  Output:
    - class (list of int)
  '''
  return [np.argmax(pred) for pred in model.predict(data)]

test_set = pd.read_csv('assets/training_data.csv', delimiter='␟', quoting=3, usecols=["id", "tweet_content", "topic"])

test_set = test_set[test_set.topic.notnull()]

test_set['Labels'] = test_set['topic'].map({'Health': 0,
                                    'Politics': 1,
                                    'Vaccines': 2,
                                    'News': 3,
                                    'Social': 4,
                                    'Lockdown': 5,
                                    'Masks': 6,
                                    'Unmarked': 7}).astype(int)

test_set.head()

text_test = test_set["tweet_content"]

text_test = np.asarray(text_test).astype('str')
tf.cast(text_test, dtype=tf.string)

y_pred = predict_class(text_test)

# %%

print(classification_report(test_set["Labels"], y_pred))

class_names = ['Health', 'Politics', 'Vaccines', 'News', 'Social', 'Lockdown', 'Masks', 'Unmarked']

prediction = []
for predict in y_pred:
  prediction.append(class_names[predict])
  
test_set['Prediction'] = prediction

print(test_set)
# %%
model.save("assets/models/text_classifier_v3")