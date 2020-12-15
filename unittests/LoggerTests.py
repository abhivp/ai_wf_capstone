#!/usr/bin/env python
"""
Log tests
"""

# import model specific functions and variables
from logger import update_train_log
from logger import update_predict_log
from model import model_train
from model import model_predict
from pathlib import Path

import os
import unittest
from ast import literal_eval
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

base_dir = Path(__file__).parent
data_dir = Path(base_dir / ".." / "data" / "cs-train").resolve()
model_dir = Path(base_dir / ".." / "models").resolve()
log_dir = Path(base_dir / ".." / "logs").resolve()

class LoggerTest(unittest.TestCase):
    """
    test the essential functionality
    """

    def test_01_train(self):
        """
        ensure log file is created
        """

        log_file = os.path.join(log_dir, "train-test.log")

        model_train(data_dir, prefix='test', test=True)
        self.assertTrue(os.path.exists(log_file))

    def test_02_train(self):
        """
        ensure that content can be retrieved from log file
        """

        log_file = os.path.join(log_dir, "train-test.log")

        # update the log
        prefix = "test"
        country = "all"
        start_data = "2017-11-29"
        end_date = "2019-05-31"
        eval_test = {'rmse': 17425}
        runtime = "000:00:14"
        model_version = 0.1
        model_version_note = "supervised learning model for time-series"
        test = True

        update_train_log(prefix, country, start_data, end_date, eval_test, runtime,
                         model_version, model_version_note, test=test)

        df = pd.read_csv(log_file)
        logged_eval_test = [literal_eval(i) for i in df['eval_test'].copy()][-1]
        self.assertEqual(eval_test, logged_eval_test)

    def test_03_predict(self):
        """
        ensure log file is created
        """

        log_file = os.path.join(log_dir, "predict-test.log")
        # if os.path.exists(log_file):
        #     os.remove(log_file)

        # update the log
        prefix = 'test'
        country = 'all'
        year = '2018'
        month = '01'
        day = '05'
        test = True
        result = model_predict(prefix, country, year, month, day, test=test)
        self.assertTrue(os.path.exists(log_file))

    def test_04_predict(self):
        """
        ensure that content can be retrieved from log file
        """

        log_file = os.path.join(log_dir, "predict-test.log")

        # update the log
        prefix = 'unittest'
        country = "all"
        y_pred = [184154.256]
        y_proba = None
        target_date = "2018-01-05"
        runtime = "000:00:35"
        model_version = 0.1
        test = True

        update_predict_log(prefix, country, y_pred, y_proba, target_date, runtime, model_version, test=test)

        df = pd.read_csv(log_file)
        logged_y_pred = [literal_eval(i) for i in df['y_pred'].copy()][-1]
        self.assertEqual(y_pred, logged_y_pred)


# Run the tests
if __name__ == '__main__':
    unittest.main()
