import tensorflow as tf
import csv

model = tf.keras.models.load_model("assets/models/text_classifier_v1.keras")

with open('assets/data/model_data.csv', 'w+', encoding="utf8") as f:
    f.write()

for x in range(1, 11):
    with open('assets/random_sample_' + str(x) + '.csv', 'r+', encoding="utf8") as file:
        reader = csv.reader((x.replace('\0', '') for x in file), delimiter='␟')
        headers = next(reader)
        for row in reader:
            with open('assets/data/model_data.csv', 'a', encoding="utf8") as f:
                f.write(row[1] + "␟" + model.predict(row[1]) + '\n')
