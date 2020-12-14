
# import model specific functions and variables
from model import model_train
from model import model_load
from model import model_predict
from model import DATA_DIR
from model import LOG_DIR

import argparse
from flask import Flask, jsonify, request
from flask import render_template, send_from_directory
import os
import re
import numpy as np

app = Flask(__name__)

@app.route("/")
def landing():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/running', methods=['POST'])
def running():
    return render_template('running.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    """
    basic predict function for the API
    """

    # input checking
    if not request.json:
        print("ERROR: API (predict): did not receive request data")
        return jsonify([])

    if 'country' not in request.json:
        print("ERROR API (predict): received request, but no 'country' found within")
        return jsonify([])

    # set the test flag
    test = False
    if 'mode' in request.json and request.json['mode'] == 'test':
        test = True

    # extract the query parameters
    prefix = request.json['prefix']
    country = request.json['country']
    year = request.json['year']
    month = request.json['month']
    day = request.json['day']


    # load model
    all_data, all_models = model_load(country, prefix, data_dir=DATA_DIR, training=False)
    model = all_models[country]

    if not model:
        print("ERROR: model is not available")
        return jsonify([])
    _result = model_predict(prefix, country, year, month, day, test=test)
    result = {}

    # convert numpy objects to ensure they are serializable
    for key, item in _result.items():
        if isinstance(item, np.ndarray):
            result[key] = item.tolist()
        else:
            result[key] = item

    return (jsonify(result))


@app.route('/train', methods=['GET', 'POST'])
def train():
    """
    basic predict function for the API

    the 'mode' flag provides the ability to toggle between a test version and a
    production verion of training
    """

    # check for request data
    if not request.json:
        print("ERROR: API (train): did not receive request data")
        return jsonify(False)

    # set the test flag
    test = False
    if 'mode' in request.json and request.json['mode'] == 'test':
        test = True

    print("... training model")
    print(DATA_DIR)
    model = model_train(data_dir=DATA_DIR, prefix='test', test=test)
    print("... training complete")

    return (jsonify(True))


@app.route('/logs/<filename>', methods=['GET'])
def logs(filename):
    """
    API endpoint to get logs
    """

    if not re.search(".log", filename):
        print("ERROR: API (log): file requested was not a log file: {}".format(filename))
        return jsonify([])

    if not os.path.isdir(LOG_DIR):
        print("ERROR: API (log): cannot find log dir")
        return jsonify([])

    file_path = os.path.join(LOG_DIR, filename)
    if not os.path.exists(file_path):
        print("ERROR: API (log): file requested could not be found: {}".format(filename))
        return jsonify([])

    return send_from_directory(LOG_DIR, filename, as_attachment=True)


if __name__ == '__main__':

    # parse arguments for debug mode
    ap = argparse.ArgumentParser()
    ap.add_argument("-d", "--debug", action="store_true", help="debug flask")
    args = vars(ap.parse_args())

    if args["debug"]:
        app.run(debug=True, port=8080)
    else:
        app.run(host='0.0.0.0', threaded=True, port=8080)
