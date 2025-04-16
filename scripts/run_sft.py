from trl import SFTTrainer
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments
from peft import LoraConfig, get_peft_model
import json
from datasets import Dataset
from transformers import DataCollatorForLanguageModeling

# 加载模型和 tokenizer
model_path = "/mnt/workspace/.cache/modelscope/models/Qwen/Qwen2___5-7B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True)

# LoRA 配置
peft_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules="all-linear",  # 根据模型需要调整
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, peft_config)

# 加载数据
def load_data(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

dataset = load_data("data\test.jsonl")

# 转换数据格式
def to_prompt(example):
    messages = example["messages"]
    prompt = ""
    for m in messages:
        prompt += f"{m['role']}: {m['content']}\n"
    return {"text": prompt.strip()}

processed = list(map(to_prompt, dataset))

# 转换为 Hugging Face Dataset
ds = Dataset.from_list(processed)

# 配置训练参数
training_args = TrainingArguments(
    output_dir="./output",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=5e-5,
    num_train_epochs=1,
    logging_dir='./logs',
    logging_steps=10,
    save_steps=500,
    save_total_limit=2,
    fp16=True,
    report_to="tensorboard",  # 使用 TensorBoard 来报告日志
    logging_first_step=True,
)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,
)

# 设置 SFTTrainer
trainer = SFTTrainer(
    model=model,
    data_collator=data_collator,
    train_dataset=ds,
    args=training_args,
    max_seq_length=1024,
)

# 启动训练
trainer.train()

# 保存adapter
trainer.model.save_pretrained("./output")