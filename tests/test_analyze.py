import os
import json
import pytest
from utils.analyze import *
import unittest
from utils.analyze import call_grammar_checking_api
from utils.analyze import parse_json

        
class TestRemoveTags(unittest.TestCase):
    def test_remove_tags(self):
        # Test case 1: Text with both add and delete tags
        text = "SpecInfer使用基于树的并行解码来计算~~其树~~##词元树的##注意力，为了能够在词元树上进行并行化验证，SpecInfer提出了一种树形注意力（Tree Attention）计算方法，通过构造的掩码矩阵和基于深度优先的KV-缓存更新机制，验证器可以在不增加额外存储的同时，尽可能并行化树中每一条路径的解码过程。相比于朴素的逐序列或逐词元~~的~~解码方法，该方法可以同时在内存开销和计算效率上达到性能最优。对于给定的推测词元树N，SpecInfer使用基于树的并行解码来计算~~其~~树形注意力，并生成一个输出张量O，~~该张量为~~##其中包含树中####每个节点u##N~~中~~的~~每个节点u~~都包含一个词元~~##对应的一个标记##。SpecInfer的词元树验证器对照大语言模型检查推测词元的正确性，SpecInfer同时支持贪心解码和~~随机采样~~##推测解码##。"
        
        print(remove_tags(text))
        
        
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
        
class TestWriteJson(unittest.TestCase):
    def test_write_json(self):
        # Mock data to write
        mock_data = {"key": "value", "list": [1, 2, 3]}
        mock_file_path = "test_output.json"

        try:
            # Call the function under test
            write_json(mock_data, mock_file_path)

            # Verify the file was created and contains the correct data
            with open(mock_file_path, 'r', encoding='utf-8') as f:
                written_data = json.load(f)
            self.assertEqual(written_data, mock_data)
        finally:
            # Clean up the test file
            if os.path.exists(mock_file_path):
                os.remove(mock_file_path)



