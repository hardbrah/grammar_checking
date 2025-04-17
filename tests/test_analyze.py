import os
import json
import pytest
from utils.analyze import remove_tags, read_json
import unittest
from utils.analyze import call_grammar_checking_api
from utils.analyze import parse_json

        
class TestRemoveTags(unittest.TestCase):
    def test_remove_tags(self):
        # Test case 1: Text with both add and delete tags
        text = "This is ##added## text and ~~deleted~~ text."
        expected = "This is added text and  text."
        self.assertEqual(remove_tags(text), expected)

        # Test case 2: Text with only add tags
        text = "This is ##added## text."
        expected = "This is added text."
        self.assertEqual(remove_tags(text), expected)

        # Test case 3: Text with only delete tags
        text = "This is ~~deleted~~ text."
        expected = "This is  text."
        self.assertEqual(remove_tags(text), expected)

        # Test case 4: Text with no tags
        text = "This is plain text."
        expected = "This is plain text."
        self.assertEqual(remove_tags(text), expected)

        # Test case 5: Empty string
        text = ""
        expected = ""
        self.assertEqual(remove_tags(text), expected)

        # Test case 6: Nested tags (edge case)
        text = "This is ##added ~~nested~~## text."
        expected = "This is added  text."
        self.assertEqual(remove_tags(text), expected)
        
        
class TestParseJson(unittest.TestCase):
    def test_parse_json(self):
        # Mock data to simulate input
        mock_data = [
            {
                "messages": [
                    {"role": "user", "content": "This is text and deleted text."},
                    {"role": "assistant", "content": "This is ##added## text and ~~deleted~~ text."}
                ]
            }
        ]

        # Expected results
        expected_results = [
            {
                "raw_text": "This is text and deleted text.",
                "ans_text": "This is ##added## text and ~~deleted~~ text.",
                "predict_text": "This is added text and  text.",
                "ans_add_count": 1,
                "ans_del_count": 1,
                "pre_add_count": 1,
                "pre_del_count": 1
            }
        ]

        # Mock the call_grammar_checking_api function
        def mock_call_grammar_checking_api(text):
            return text  # Return the input text as the mock response

        # Replace the real API call with the mock
        global call_grammar_checking_api
        call_grammar_checking_api = mock_call_grammar_checking_api

        # Call the function under test
        results, ans_adds, ans_dels, pre_adds, pre_dels = parse_json(mock_data)

        # Assertions
        self.assertEqual(results, expected_results)
        self.assertEqual(ans_adds, [1, 0])
        self.assertEqual(ans_dels, [0, 0])
        self.assertEqual(pre_adds, [1, 1])
        self.assertEqual(pre_dels, [1, 1])


