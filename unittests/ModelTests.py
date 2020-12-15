#!/usr/bin/env python
"""
model tests
"""

# import model specific functions and variables
from model import model_train
from model import model_load
from model import model_predict
from pathlib import Path

import os
import unittest
import warnings

warnings.filterwarnings("ignore")

# data_dir = os.path.join("..", "data", "cs-train")
base_dir = Path(__file__).parent
data_dir = Path(base_dir / ".." / "data" / "cs-train").resolve()
model_dir = Path(base_dir / ".." / "models").resolve()


class ModelTest(unittest.TestCase):
    """
    test the essential functionality
    """

    def test_01_train(self):
        """
        test the train functionality
        """

        # train the model
        model_train(data_dir, prefix='test', test=True)
        self.assertTrue(os.path.exists(os.path.join(model_dir, "test-all-0_1.joblib")))

    def test_02_load(self):
        """
        test the train functionality
        """

        # Load the model
        model_data, models = model_load(country='united_kingdom', prefix='test', data_dir=data_dir, training=False)
        model = list(models.values())[0]
        self.assertTrue('predict' in dir(model))
        self.assertTrue('fit' in dir(model))

    def test_03_predict(self):
        """
        test the predict function input
        """

        # load model first
        prefix = 'test'
        country = 'united_kingdom'
        year = '2018'
        month = '01'
        day = '05'
        test = True

        result = model_predict(prefix, country, year, month, day, test=test)
        y_pred = result['y_pred']
        self.assertTrue(result is not None)


### Run the tests
if __name__ == '__main__':
    unittest.main()
