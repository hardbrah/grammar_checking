from openai import OpenAI
client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed",
)

completion = client.chat.completions.create(
  model="grammar_checking",
  messages=[
    {"role": "user", "content": "最受外界关注的APEC领导人非正式会议于2018年11月12日在巴布亚新几内亚召开，APEC会议已经成为当今国际交流的平台。"},
  ],
  seed=42
)

print(completion.choices[0].message.content)