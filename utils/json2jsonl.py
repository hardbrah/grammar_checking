import json
import os

def json_to_jsonl(input_file, output_file):
    """
    Convert a JSON file to JSONL format.

    Args:
        input_file (str): Path to the input JSON file.
        output_file (str): Path to the output JSONL file.
    """
    with open(input_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for item in data:
            json.dump(item, outfile, ensure_ascii=False)
            outfile.write('\n')

            
if __name__ == "__main__":
    # input_dir = r'D:\code\数据清洗\FCGEC\output'  # Replace with your input JSON file path
    # output_dir = r'D:\code\数据清洗\FCGEC\output_jsonl'  # Replace with your desired output directory
    # os.makedirs(output_dir, exist_ok=True)
    # for filename in os.listdir(input_dir):
    #     if filename.endswith('.json'):
    #         input_file = os.path.join(input_dir, filename)
    #         output_file = os.path.join(output_dir, filename.replace('.json', '.jsonl'))
    #         json_to_jsonl(input_file, output_file)
    
    input_file = r'D:\code\grammar_checking\data\grammar_checking.json'  # Replace with your input JSON file path
    output_file = r'D:\code\grammar_checking\data\grammar_checking.jsonl'  # Replace with your desired output JSONL file path
    json_to_jsonl(input_file, output_file)