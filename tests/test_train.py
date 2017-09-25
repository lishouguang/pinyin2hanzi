# coding: utf-8

import unittest

from p2h import train


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)

    def test_train(self):
        self.assertTrue(True)

        train.train()


if __name__ == '__main__':
    unittest.main()
