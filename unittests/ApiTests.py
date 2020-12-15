#!/usr/bin/env python
"""
api tests

these tests use the requests package however similar requests can be made with curl

e.g.

data = '{"key":"value"}'
curl -X POST -H "Content-Type: application/json" -d "%s" http://localhost:8080/predict'%(data)
"""

import os
import unittest
import requests
import re
import json
from pathlib import Path
from datetime import date

base_dir = Path(__file__).parent
log_dir = Path(base_dir / ".." / "logs").resolve()

port = 8080

try:
    requests.post('http://127.0.0.1:{}/predict'.format(port))
    server_available = True
except:
    server_available = False


# test class for the main window function
class ApiTest(unittest.TestCase):
    """
    test the essential functionality
    """

    @unittest.skipUnless(server_available, "local server is not running")
    def test_01_train(self):
        """
        test the train functionality
        """

        request_json = {'mode': 'test'}
        r = requests.post('http://127.0.0.1:{}/train'.format(port), json=request_json)
        train_complete = re.sub("\W+", "", r.text)
        self.assertEqual(train_complete, 'true')

    @unittest.skipUnless(server_available, "local server is not running")
    def test_03_predict(self):
        """
        test the predict functionality
        """

        r = requests.get('http://localhost:8080/predict?country=united_kingdom&date=2019-05-05')
        check_complete = json.loads(r.text)['status']
        self.assertEqual(check_complete, 'OK')

    @unittest.skipUnless(server_available, "local server is not running")
    def test_04_logs(self):
        """
        test the log functionality
        """

        today = date.today()
        file_name = os.path.join(log_dir, "train-{}-{}.log".format(today.year, today.month))
        r = requests.get('http://127.0.0.1:{}/logs/{}'.format(port, file_name))
        self.assertTrue(os.path.exists(file_name))


# Run the tests
if __name__ == '__main__':
    unittest.main()
