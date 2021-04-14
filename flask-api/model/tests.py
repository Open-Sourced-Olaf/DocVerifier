# -*- coding: utf-8 -*-

import unittest

from predictor import predict_nb

class Tests(unittest.TestCase):
    def test_predict(self):
        self.assertAlmostEqual(predict_nb('blah'),False)
        self.assertAlmostEqual(predict_nb('We collect purchase history.'),True)
        self.assertAlmostEqual(predict_nb(''),False)
        self.assertAlmostEqual(predict_nb('Decide what types of activity you’d like saved in your account.'),False)