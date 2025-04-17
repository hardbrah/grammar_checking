import os
import json
import pytest
from utils.analyze import *
import unittest


class TestAnalyze(unittest.TestCase):
    def test_read_json(self):
        # Create a temporary JSONL file
        file_path = r"D:\code\grammar_checking\data\grammar_checking.json"
        data = read_json(file_path)
        print(f"data: {data}")
        
    def test_calculate(self):
        data = read_json(r"D:\code\grammar_checking\data\grammar_checking.json")
        ret = caculate(data[0]["messages"][1]["content"])
        print(data[0]["messages"][1]["content"])
        print(f"ret: {ret}")
