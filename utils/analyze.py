import json
import re
import os
from utils.llm_api import call_grammar_checking_api
from utils.plot_data import *

def remove_tags(text):
    """
    去除文本中的标签
    :param text: 带标签的文本
    :return: 去除标签后的文本
    """
    text = re.sub(r"##(.*?)##", r"\1", text)  # 去除添加标签
    text = re.sub(r"~~(.*?)~~", r"", text)  # 去除删除标签
    return text

def read_jsonl(file_path):
    """
    读取jsonl文件并返回数据列表
    """
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def read_json(file_path):
    """读取json文件并返回数据
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def write_json(data, file_path):
    """将数据写入json文件
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def caculate(data:str):
    """
    分析数据，统计修改符号个数
    :param data: 句子
    :return: 添加符号个数，删除符号个数
    """
    add_count, del_count = 0, 0
    add_match = re.findall(r"##(.*?)##", data)
    if add_match:
        add_count = len(add_match)
    del_match = re.findall(r"~~(.*?)~~", data)
    if del_match:
        del_count = len(del_match)
    return add_count, del_count

def parse_json(data):
    """
    分析jsonl文件，统计修改符号个数
    :param file_path: jsonl文件路径
    :return: json列表，每个元素包含原句、答案、预测结果、添加符号个数、删除符号个数
    """

    results, ans_adds, ans_dels, pre_adds, pre_dels = [], [], [], [], []
    for item in data:
        for message in item["messages"]:
            if message["role"] == "assistant":
                ans_text = message["content"]
            if message["role"] == "user":
                raw_text = message["content"]
        ret = assemble_json(raw_text, ans_text)
        results.append(ret) 
        ans_adds.append(ret["ans_add_count"])
        ans_dels.append(ret["ans_del_count"])
        pre_adds.append(ret["pre_add_count"])
        pre_dels.append(ret["pre_del_count"])
    return results, ans_adds, ans_dels, pre_adds, pre_dels

def assemble_json(raw_text, ans_text):
    predict_text = call_grammar_checking_api(raw_text)
    no_tag_predict_text = remove_tags(predict_text)
    no_tag_ans_text = remove_tags(ans_text)
    ans_add_count, ans_del_count = caculate(ans_text)
    pre_add_count, pre_del_count = caculate(predict_text)
    return {"raw": raw_text,"ans_text":ans_text,"predict_text":predict_text, "no_tag_ans_text":no_tag_ans_text, "no_tag_predict_text":no_tag_predict_text, "ans_add_count":ans_add_count, "ans_del_count": ans_del_count, "pre_add_count": pre_add_count, "pre_del_count": pre_del_count}

def calculate_statistics(ans_adds, ans_dels, pre_adds, pre_dels):
    # 比较修改次数是否都相同
    cnt_add, cnt_del, cnt_same = 0, 0, 0
    for i, j, k, z in zip(ans_adds, pre_adds, ans_dels, pre_dels):
        if i == j:
            cnt_add += 1
        if k == z:
            cnt_del += 1
        if i == j and k == z:
            cnt_same += 1

    print(f"修改次数相同：{cnt_same}，添加次数相同：{cnt_add}，删除次数相同：{cnt_del}")
    print(f"修改次数相同占比：{cnt_same / len(ans_adds)}，添加次数相同占比：{cnt_add / len(ans_adds)}，删除次数相同占比：{cnt_del / len(ans_adds)}")


    

if __name__ == "__main__":
    # 示例用法
    results, ans_adds, ans_dels, pre_adds, pre_dels = [], [], [], [], []
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, '..', 'data', 'grammar_checking.json')
    output_dir = os.path.join(base_dir, '..', 'data', 'grammar_checking_results.json')
    results, ans_adds, ans_dels, pre_adds, pre_dels = parse_json(read_json(file_path))
    ans_modify_times = [ans_add + ans_del for ans_add, ans_del in zip(ans_adds, ans_dels)]
    pre_modify_times = [pre_add + pre_del for pre_add, pre_del in zip(pre_adds, pre_dels)]
    write_json(results, output_dir)


    with open(os.path.join(base_dir, 'mydata.txt'), 'w', encoding='utf-8') as f:
        # 转换成json格式
        json.dump({"ans_adds": ans_adds, "ans_dels": ans_dels, "pre_adds": pre_adds, "pre_dels": pre_dels, "ans_modify_times": ans_modify_times, "pre_modify_times": pre_modify_times}, f, ensure_ascii=False)
    
    # 绘制图
    plot_scatter(ans_adds, pre_adds, x_label="ans_add_count", y_label="pre_add_count", title="relationship between ans_add_count and pre_add_count", file_path=os.path.join(base_dir, '..', 'images', 'adds_scatter_chart.png'))
    plot_scatter(ans_dels, pre_dels, x_label="ans_del_count", y_label="pre_del_count", title="relationship between ans_del_count and pre_del_count", file_path=os.path.join(base_dir, '..', 'images', 'dels_scatter_chart.png'))
    plot_scatter(ans_modify_times, pre_modify_times, x_label="ans_modify_times", y_label="pre_modify_times", title="relationship between ans_modify_times and pre_modify_times", file_path=os.path.join(base_dir, '..', 'images', 'modify_times_scatter_chart.png'))

    
    print("分析完成，结果已保存。")
    