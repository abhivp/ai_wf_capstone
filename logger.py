#!/usr/bin/env python
"""
module with functions to enable logging
"""

import csv
import os
import time
import uuid
from datetime import date
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

base_dir = Path(__file__).parent
# MODEL_DIR = "models"
DATA_DIR = Path(base_dir / "data" / "cs-train").resolve()
MODEL_DIR = Path(base_dir / "models").resolve()
LOG_DIR = Path(base_dir / "logs").resolve()
MODEL_VERSION = 0.1
MODEL_VERSION_NOTE = "supervised learning model for time-series"

# if not os.path.exists(os.path.join(".", "logs")):
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)


def update_train_log(prefix, country, start_data, end_date, eval_test, runtime,
                     model_version, model_version_note, test=False):
    """
    update train log file
    """

    # name the logfile using something that cycles with date (day, month, year)
    today = date.today()
    if test:
        logfile = os.path.join(LOG_DIR, "train-test.log")
    else:
        logfile = os.path.join(LOG_DIR, "train-{}-{}.log".format(today.year, today.month))

    # write the data to a csv file
    header = ['Run_Date', 'unique_id', 'time_stamp', 'prefix', 'Country', 'Range Start Date', 'Range End Date',
              'eval_test', 'RunTime', 'Model_Version', 'Model_Version_Note', 'Test']
    write_header = False
    if not os.path.exists(logfile):
        write_header = True
    with open(logfile, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        if write_header:
            writer.writerow(header)

        to_write = map(str, [today, uuid.uuid4(), time.time(), prefix, country, start_data, end_date,
                             eval_test, runtime, model_version, model_version_note, test])
        writer.writerow(to_write)


def update_predict_log(prefix, country, y_pred, y_proba, target_date, runtime, model_version, test=False):
    """
    update predict log file
    """

    ## name the logfile using something that cycles with date (day, month, year)    
    today = date.today()
    if test:
        logfile = os.path.join(LOG_DIR, "predict-test.log")
    else:
        logfile = os.path.join(LOG_DIR, "predict-{}-{}.log".format(today.year, today.month))

    # write the data to a csv file
    header = ['Run_Date', 'unique_id', 'time_stamp', 'Prefix', 'Country', 'y_pred', 'y_proba', 'Target_Date', 'Runtime',
              'model_version', 'Test']
    write_header = False
    if not os.path.exists(logfile):
        write_header = True
    with open(logfile, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        if write_header:
            writer.writerow(header)

        to_write = map(str, [today, uuid.uuid4(), time.time(), prefix, country, y_pred, y_proba, target_date, runtime,
                             model_version, test])
        writer.writerow(to_write)


if __name__ == "__main__":
    """
    basic test procedure for logger.py
    """

    from model import MODEL_VERSION, MODEL_VERSION_NOTE

    ## train logger
    # update the log
    prefix = "unittest"
    country = "all"
    start_data = "2017-11-29"
    end_date = "2019-05-31"
    eval_test = {'rmse': 17425}
    runtime = "000:00:14"
    model_version = 0.1
    model_version_note = "supervised learning model for time-series"
    test = False

    update_train_log(prefix, country, start_data, end_date, eval_test, runtime,
                     model_version, model_version_note, test=test)

    # predict logger
    prefix = 'unittest'
    country = "all"
    y_pred = [184154.256]
    y_proba = None
    target_date = "2018-01-05"
    runtime = "000:00:35"
    model_version = 0.1
    test = False

    update_predict_log(prefix, country, y_pred, y_proba, target_date, runtime, model_version, test=test)
