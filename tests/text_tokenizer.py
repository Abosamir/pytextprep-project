import unittest
from pytextprep.steps import tokenizer

class TestWordTokenize(unittest.TestCase):

    def test_basic_with_punctuation(self):
        result = tokenizer.word_tokenize("Hello, world!")
        self.assertEqual(result, ["Hello", "world"])

    def test_contraction_and_hyphen(self):
        result = tokenizer.word_tokenize("don't use state-of-the-art")
        self.assertEqual(result, ["don't", "use", "state-of-the-art"])
        
    def test_empty_string(self):
        self.assertEqual(tokenizer.word_tokenize(""), [])

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            tokenizer.word_tokenize(123)


class TestSentTokenize(unittest.TestCase):

    def test_basic_split(self):
        result = tokenizer.sent_tokenize("Hello world. How are you? Fine!")
        self.assertEqual(result, ["Hello world.", "How are you?", "Fine!"])

    def test_abbreviation_not_split(self):
        result = tokenizer.sent_tokenize("Dr. Smith is here. He is late.")
        self.assertEqual(result, ["Dr. Smith is here.", "He is late."])

    def test_decimal_not_split(self):
        result = tokenizer.sent_tokenize("Pi is 3.14. Use e.g. this one!")
        self.assertEqual(result, ["Pi is 3.14.", "Use e.g. this one!"])

    def test_non_string_raises(self):
        with self.assertRaises(TypeError):
            tokenizer.sent_tokenize(None)


if __name__ == "__main__":
    unittest.main()