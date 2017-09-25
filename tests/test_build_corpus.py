# coding: utf-8

import unittest

from p2h.build_corpus import build_corpus


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)

    def test_build_corpus(self):
        self.assertTrue(True)
        build_corpus()

if __name__ == '__main__':
    unittest.main()
