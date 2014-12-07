import unittest
import json
import numpy

from brain_data import BrainData


class TestBrainData(unittest.TestCase):

    def setUp(self):
        self.path = 'data/data_v2.json'
        raw_data = json.load(open(self.path))
        self.brain = BrainData(raw_data)

    def test_load(self):
        self.assertEqual(len(self.brain.data), 1845)
        self.assertEqual(type(self.brain.data), numpy.ndarray)
        self.assertEqual(len(self.brain.data[0]), 16)
        self.assertEqual(self.brain.name, 'subj1_16regions_1845time')


if __name__ == '__main__':
    unittest.main()
