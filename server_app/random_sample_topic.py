import csv
import tensorflow as tf
from keras import backend as K
import tensorflow_text as text
import numpy as np

def predict(data):
    return [np.argmax(pred) for pred in model.predict(data)]

def predict_and_class(data):
    text_data = np.asarray(data).astype('str')
    tf.cast(text_data, dtype=tf.string)
    prediction = predict(text_data)
    class_names = ['Health', 'Politics', 'Vaccines', 'News', 'Social', 'Lockdown', 'Unmarked']
    predicitions = []
    for pred in prediction:
        predicitions.append(class_names[pred])
    
    return predicitions

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

model = tf.keras.models.load_model('assets/models/text_classifier_v2', custom_objects = {"balanced_recall": balanced_recall, "balanced_precision": balanced_precision, "balanced_f1_score": balanced_f1_score})

for x in range(1, 16):
    with open('assets/random_sample_' + str(x) +'_topic.csv', 'w+', encoding="utf8") as f:
        with open('assets/random_sample_' + str(x) +'.csv', 'r+', encoding="utf8") as file:
            reader = csv.reader((x.replace('\0', '') for x in file), delimiter='␟')
            headers = next(reader)
            headers.append("topic")
            for x in range(0, len(headers)):
                if x == len(headers) - 1:
                    f.write(str(headers[x]) + '\n')
                else:
                    f.write(str(headers[x]) + '␟')
            
            values = []
            
            for row in reader:
                if len(row) < 10:
                    continue
                values.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]])
            
            topics = predict_and_class([x[1] for x in values])

            for x in range(0, len(values)):
                value = values[x]
                value.append(topics[x])
                for x in range(0, len(value)):
                    if x == len(value) - 1:
                        f.write(str(value[x]) + '\n')
                    else:
                        f.write(str(value[x]) + '␟')