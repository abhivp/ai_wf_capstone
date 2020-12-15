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
import time
from datetime import datetime as dt

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


@app.route('/predict', methods=['GET'])
def predict():
    """
    basic predict function for the API

    country='all'
    year='2019'
    month='04'
    day='06'
    2017-11-29    2019-05-31
    """
    run_start = time.time()

    country = request.args.get('country', default='all', type=str)
    date = request.args.get('date', default='2019-05-06', type=str)
    startDate = dt.strptime("2017-11-29", "%Y-%m-%d")
    endDate = dt.strptime("2019-05-31", "%Y-%m-%d")
    try:
        predictDate = dt.strptime(date, "%Y-%m-%d")
    except:
        return jsonify(errMsg='Error Date, date should be in range 2017-11-29  -  2019-05-31')

    if startDate <= predictDate < endDate:
        dataSplit = date.split('-')
        year = dataSplit[0]
        month = dataSplit[1]
        day = dataSplit[2]
        try:
            result = model_predict(prefix='sl', country=country, year=year, month=month, day=day)
        except:
            return jsonify(msg='model_predict error')
        m, s = divmod(time.time() - run_start, 60)
        h, m = divmod(m, 60)

        return jsonify(status='OK', date=date, country=country, y_pred=result['y_pred'][0],
                       runningTime="%d:%02d:%02d" % (h, m, s), )
    else:
        return jsonify(errMsg='Error Date, date should be in range 2017-11-29  -  2019-05-31')


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
