from unittest import TestCase

from SimpleParser import SimpleParser


class TestSimpleParser(TestCase):

    def test_parseIntToTuple(self):
        self.assertTupleEqual((2, 0), SimpleParser.parseIntToTuple(7))
        self.assertTupleEqual((1, 1), SimpleParser.parseIntToTuple(5))
        self.assertTupleEqual((0, 2), SimpleParser.parseIntToTuple(3))
        self.assertTupleEqual((1, 2), SimpleParser.parseIntToTuple(6))
        self.assertTupleEqual((3, 0), SimpleParser.parseIntToTuple(10))
