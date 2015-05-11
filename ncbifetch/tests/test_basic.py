# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
from ncbifetch import main
import unittest


class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test_absolute_truth_and_meaning(self):
        assert True

    def test_test(self):
        assert main.x() == 'ping'

    def test_sal_wgs(self):
        main.fetch_wgs(organism='Salmonella enterica')
        assert True


if __name__ == '__main__':
    unittest.main()