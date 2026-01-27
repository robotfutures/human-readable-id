import unittest
from unittest import mock

import hrid
from hrid import NICE_WORD_LISTS
from hrid.word_lists.nice import WORD_LISTS as NICE_LISTS


class TestGenerateFunction(unittest.TestCase):

    def setUp(self):
        self.hrid = hrid.HRID()
        self.hrid.delimiter = ', '
        self.hrid.random = mock.Mock()
        self.hrid.random.choice.side_effect = lambda x: x[0]

    def test_transform_string_element(self):
        element = 'adjective'
        expected_output = hrid.WORD_LISTS['adjective']
        self.assertEqual(self.hrid._transform_element(element), expected_output)

    def test_transform_list_element(self):
        element = ['hello', 'hi']
        self.assertEqual(self.hrid._transform_element(element), element)

    def test_transform_unknown_element(self):
        element = 'unknown'
        expected_output = [element]
        self.assertEqual(self.hrid._transform_element(element), expected_output)

    def test_string_elements_only(self):
        self.hrid._elements = [['hello'], ['world']]
        expected_output = 'hello, world'
        self.assertEqual(self.hrid.generate(), expected_output)

    def test_list_elements_only(self):
        self.hrid._elements = [['hello', 'hi'], ['world', 'earth']]
        expected_output = 'hello, world'
        self.assertEqual(self.hrid.generate(), expected_output)

    def test_mixed_string_and_list_elements(self):
        self.hrid._elements = [['hello'], ['world', 'earth'], ['again']]
        expected_output = 'hello, world, again'
        self.assertEqual(self.hrid.generate(), expected_output)

    def test_empty_elements(self):
        self.hrid._elements = []
        expected_output = ''
        self.assertEqual(self.hrid.generate(), expected_output)

    def test_none_elements(self):
        self.hrid._elements = None
        with self.assertRaises(TypeError):
            self.hrid.generate()


class TestCustomWordLists(unittest.TestCase):

    def test_custom_word_lists_parameter(self):
        custom_lists = {
            'greeting': ['hello', 'hi', 'hey'],
            'target': ['world', 'universe', 'everyone'],
        }
        h = hrid.HRID(elements=('greeting', 'target'), word_lists=custom_lists, seed=42)
        result = h.generate()
        parts = result.split('-')
        self.assertEqual(len(parts), 2)
        self.assertIn(parts[0], custom_lists['greeting'])
        self.assertIn(parts[1], custom_lists['target'])

    def test_nice_word_lists_parameter(self):
        h = hrid.HRID(elements=('weather', 'fabric', 'place'), word_lists=NICE_WORD_LISTS, seed=42)
        result = h.generate()
        parts = result.split('-')
        self.assertEqual(len(parts), 3)
        self.assertIn(parts[0], NICE_WORD_LISTS['weather'])
        self.assertIn(parts[1], NICE_WORD_LISTS['fabric'])
        self.assertIn(parts[2], NICE_WORD_LISTS['place'])

    def test_nice_word_lists_new_categories(self):
        h = hrid.HRID(elements=('tree', 'place'), word_lists=NICE_WORD_LISTS, seed=123)
        result = h.generate()
        parts = result.split('-')
        self.assertEqual(len(parts), 2)
        self.assertIn(parts[0], NICE_WORD_LISTS['tree'])
        self.assertIn(parts[1], NICE_WORD_LISTS['place'])

    def test_default_word_lists_when_none(self):
        h = hrid.HRID(word_lists=None)
        self.assertEqual(h.word_lists, hrid.WORD_LISTS)


class TestNiceWordLists(unittest.TestCase):

    def test_nice_word_lists_exported(self):
        self.assertIsInstance(NICE_WORD_LISTS, dict)
        self.assertIn('adjective', NICE_WORD_LISTS)
        self.assertIn('noun', NICE_WORD_LISTS)
        self.assertIn('verb', NICE_WORD_LISTS)
        self.assertIn('adverb', NICE_WORD_LISTS)

    def test_nice_word_lists_has_new_categories(self):
        self.assertIn('place', NICE_WORD_LISTS)
        self.assertIn('tree', NICE_WORD_LISTS)
        self.assertIn('weather', NICE_WORD_LISTS)
        self.assertIn('fabric', NICE_WORD_LISTS)
        self.assertIn('mood', NICE_WORD_LISTS)

    def test_nice_word_lists_not_empty(self):
        for key, words in NICE_WORD_LISTS.items():
            self.assertGreater(len(words), 0, f"Word list '{key}' should not be empty")

    def test_places_contains_expected_words(self):
        places = NICE_WORD_LISTS['place']
        expected = ['meadow', 'lighthouse', 'cottage', 'oasis', 'villa']
        for word in expected:
            self.assertIn(word, places)

    def test_trees_contains_expected_words(self):
        trees = NICE_WORD_LISTS['tree']
        expected = ['oak', 'maple', 'willow', 'cedar', 'birch']
        for word in expected:
            self.assertIn(word, trees)

    def test_weather_contains_expected_words(self):
        weather = NICE_WORD_LISTS['weather']
        expected = ['rainbow', 'sunrise', 'breeze', 'aurora', 'snowflake']
        for word in expected:
            self.assertIn(word, weather)

    def test_fabrics_contains_expected_words(self):
        fabrics = NICE_WORD_LISTS['fabric']
        expected = ['velvet', 'silk', 'cotton', 'denim', 'cashmere']
        for word in expected:
            self.assertIn(word, fabrics)

    def test_no_negative_words_in_nice_adjectives(self):
        adjectives = NICE_WORD_LISTS['adjective']
        negative_words = [
            'angry', 'depressed', 'hopeless', 'miserable', 'stupid',
            'ugly', 'worthless', 'aggressive', 'hostile', 'violent'
        ]
        for word in negative_words:
            self.assertNotIn(word, adjectives, f"'{word}' should not be in nice adjectives")


class TestSeedReproducibility(unittest.TestCase):

    def test_same_seed_produces_same_result(self):
        h1 = hrid.HRID(seed=12345)
        h2 = hrid.HRID(seed=12345)
        self.assertEqual(h1.generate(), h2.generate())

    def test_different_seeds_produce_different_results(self):
        h1 = hrid.HRID(seed=12345)
        h2 = hrid.HRID(seed=54321)
        # While not guaranteed, these should almost certainly differ
        results1 = [h1.generate() for _ in range(10)]
        results2 = [h2.generate() for _ in range(10)]
        self.assertNotEqual(results1, results2)

    def test_seed_with_nice_word_lists(self):
        h1 = hrid.HRID(elements=('weather', 'tree'), word_lists=NICE_WORD_LISTS, seed=999)
        h2 = hrid.HRID(elements=('weather', 'tree'), word_lists=NICE_WORD_LISTS, seed=999)
        self.assertEqual(h1.generate(), h2.generate())


if __name__ == '__main__':
    unittest.main()
