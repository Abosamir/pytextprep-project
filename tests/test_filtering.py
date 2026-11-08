from pytextprep.steps import filtering
import unittest


class TestNormalization(unittest.TestCase):

    # remove_stopwords
    def test_remove_stopwords(self):
        result = filtering.remove_stopwords("")
        self.assertEqual(result, "")

    def test_remove_stopwords_basic(self):
        result = filtering.remove_stopwords("this is a good movie")
        self.assertEqual(result, "good movie")

    def test_remove_stopwords_custom_words(self):
        result = filtering.remove_stopwords("this is a good movie", custom_words=["movie"])
        self.assertEqual(result, "good")

    def test_remove_stopwords_extra_only(self):
        result = filtering.remove_stopwords("this is a good movie", custom_words=["movie"], extra_only=True)
        self.assertEqual(result, "this is a good")

    def test_remove_stopwords_extra_only_no_custom(self):
        result = filtering.remove_stopwords("this is a good movie", extra_only=True)
        self.assertEqual(result, "this is a good movie")

    def test_remove_stopwords_only_stopwords(self):
        result = filtering.remove_stopwords("this is a")
        self.assertEqual(result, "")

    def test_remove_stopwords_not_str(self):
        with self.assertRaises(TypeError):
            filtering.remove_stopwords(123)

    # expand_contractions
    def test_expand_contractions(self):
        result = filtering.expand_contractions("")
        self.assertEqual(result, "")

    def test_expand_contractions_basic(self):
        result = filtering.expand_contractions("don't worry")
        self.assertEqual(result, "do not worry")

    def test_expand_contractions_no_contractions(self):
        result = filtering.expand_contractions("They’re here") 
        self.assertEqual(result, "They are here")

    def test_expand_contractions_not_str(self):
        with self.assertRaises(TypeError):
            filtering.expand_contractions(None)


if __name__ == "__main__":
    unittest.main()