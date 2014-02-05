import unittest
import os

from repetition import RepetitionAnalyzer

class TestRepetitionAnalysis(unittest.TestCase):
    def setUp(self):
        self.analyzer = RepetitionAnalyzer('fixtures')

    def test_analysis(self):
        self.analyzer.analyze()

    def test_detect_repetition(self):
        input_file = open('fixtures/sample.txt')
        output_file = os.tmpfile()
        repetitions = self.analyzer.create_repetition_dictionary()
        self.analyzer.detect_repetition(15, input_file, output_file, repetitions)

if __name__ == '__main__':
    unittest.main()
