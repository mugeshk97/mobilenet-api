from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
import json
import base64
import io
from imageio import imread



gpu = tf.config.experimental.list_physical_devices('GPU')

if len(gpu) == 1:
    tf.config.experimental.set_memory_growth(gpu[0], True)
else:
    pass

model = tf.keras.applications.mobilenet_v2.MobileNetV2()

class_file = open('imagenet_class_index.json')
label_data = json.load(class_file)


app = Flask(__name__)


@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.get_json()
        b64_img = io.BytesIO(base64.b64decode(data['bytes']))
        img = imread(b64_img)
        img = tf.keras.preprocessing.image.smart_resize(img, size=(224,224))
        img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
        img = tf.expand_dims(img, axis= 0)
        prediction = model.predict(img)
        label_index = np.argmax(prediction)
        predicted_cls = label_data[str(label_index)]
        predicted_prob = prediction[0][label_index]
        resp = {'result': predicted_cls, 'prob': str(predicted_prob)}

    return resp


if __name__ == '__main__':
	app.run(debug=True, host = '0.0.0.0', port = 5001)