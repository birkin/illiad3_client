"""
To test all...
$ python3 ./test.py

To run specific test...
$ python3 ./test/account.py AccountTest.test_logout
"""

import logging, unittest
from test import account_test
from test import parser_test


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(account_test.suite())
    test_suite.addTest(parser_test.suite())
    return test_suite

runner = unittest.TextTestRunner()
runner.run(suite())
