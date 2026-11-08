import unittest

from pytextprep.steps import cleaning



class TestCleaning(unittest.TestCase):

    # lower_case
    def test_lower_case(self):
        result = cleaning.lower_case("")
        self.assertEqual(result, "")

    def test_lower_case_mixed(self):
        result = cleaning.lower_case("HeLLo World")
        self.assertEqual(result, "hello world")

    def test_lower_case_not_str(self):
        with self.assertRaises(TypeError):
            cleaning.lower_case(42)

    # normalize_whitespace
    def test_normalize_whitespace(self):
        result = cleaning.normalize_whitespace("")
        self.assertEqual(result, "")

    def test_normalize_whitespace_tabs_newlines(self):
        result = cleaning.normalize_whitespace("hello   world\t\tagain\n\nend")
        self.assertEqual(result, "hello world again end")

    def test_normalize_whitespace_not_str(self):
        with self.assertRaises(TypeError):
            cleaning.normalize_whitespace(None)

    # remove_urls
    def test_remove_urls(self):
        result = cleaning.remove_urls("")
        self.assertEqual(result, "")

    def test_remove_urls_http(self):
        result = cleaning.remove_urls("go to https://a.io/x?y=1.")
        self.assertEqual(result, "go to .")

    def test_remove_urls_www(self):
        result = cleaning.remove_urls("not a url: http:/broken")
        self.assertEqual(result, "not a url: http:/broken")

    def test_remove_urls_replace_with(self):
        result = cleaning.remove_urls("visit https://example.com now", replace_with="<URL>")
        self.assertEqual(result, "visit <URL> now")

    def test_remove_urls_not_str(self):
        with self.assertRaises(TypeError):
            cleaning.remove_urls(["https://example.com"])

    # remove_emails
    def test_remove_emails(self):
        result = cleaning.remove_emails("")
        self.assertEqual(result, "")

    def test_remove_emails_basic(self):
        result = cleaning.remove_emails("write to ali@iti.gov.eg today")
        self.assertEqual(result, "write to today")

    def test_remove_emails_not_str(self):
        with self.assertRaises(TypeError):
            cleaning.remove_emails(42)

    # is_emoji
    def test_is_emoji(self):
        result = cleaning.is_emoji("😀")
        self.assertTrue(result)

    def test_is_emoji_letter(self):
        result = cleaning.is_emoji("a")
        self.assertFalse(result)

    def test_is_emoji_punctuation(self):
        result = cleaning.is_emoji("!")
        self.assertFalse(result)

    def test_is_emoji_empty(self):
        with self.assertRaises(TypeError):
            cleaning.is_emoji("")

    def test_is_emoji_not_str(self):
        with self.assertRaises(TypeError):
            cleaning.is_emoji(1)

    # remove_punctuation
    def test_remove_punctuation(self):
        result = cleaning.remove_punctuation("")
        self.assertEqual(result, "")

    def test_remove_punctuation_basic(self):
        result = cleaning.remove_punctuation("hello, world!")
        self.assertEqual(result, "hello  world ")

    def test_remove_punctuation_keeps_nt(self):
        result = cleaning.remove_punctuation("don't")
        self.assertEqual(result, "don't")

    def test_remove_punctuation_keep_emojis(self):
        result = cleaning.remove_punctuation("hi 😀!")
        self.assertEqual(result, "hi 😀 ")

    def test_remove_punctuation_drop_emojis(self):
        result = cleaning.remove_punctuation("hi 😀!", keep_emojis=False)
        self.assertEqual(result, "hi  ")

    def test_remove_punctuation_not_str(self):
        with self.assertRaises(TypeError):
            cleaning.remove_punctuation(42)

    # normalize_repeating_chars
    def test_normalize_repeating_chars(self):
        result = cleaning.normalize_repeating_chars("")
        self.assertEqual(result, "")

    def test_normalize_repeating_chars_basic(self):
        result = cleaning.normalize_repeating_chars("good book")
        self.assertEqual(result, "good book")

    def test_normalize_repeating_chars_keep_two(self):
        result = cleaning.normalize_repeating_chars("sooooo", keep=2)
        self.assertEqual(result, "soo")

    def test_normalize_repeating_chars_double_untouched(self):
        result = cleaning.normalize_repeating_chars("good")
        self.assertEqual(result, "good")

    def test_normalize_repeating_chars_not_str(self):
        with self.assertRaises(TypeError):
            cleaning.normalize_repeating_chars(None)


if __name__ == "__main__":
    unittest.main()