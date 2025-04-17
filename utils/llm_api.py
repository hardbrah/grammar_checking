from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed",
)

def call_grammar_checking_api(text):
    system_prompt_template = "你是一个中文语法纠错助手。请判断用户输入的句子是否存在语病或不符合中文表达习惯的问题。若无错，原样输出；若有错，请使用 `##添加内容##` 表示新增，`~~删除内容~~` 表示删除，仅输出修改后的句子或原句，不要解释说明。"
    user_prompt_template = "请检查以下中文句子的语法或用词是否恰当，并按照规定格式进行修改：\n\n{句子}"
    prompt = user_prompt_template.format(句子=text)
    completion = client.chat.completions.create(
    model="grammar_checking",
    messages=[
        {"role": "system", "content": system_prompt_template},
        {"role": "user", "content": prompt},
    ],
    seed=42
    )

    return completion.choices[0].message.content