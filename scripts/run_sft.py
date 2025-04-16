from trl import SFTTrainer, SFTConfig
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments
from peft import LoraConfig, get_peft_model
import json
from datasets import Dataset
from transformers import DataCollatorForLanguageModeling
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

# 加载模型和 tokenizer
model_path = "/mnt/workspace/.cache/modelscope/models/Qwen/Qwen2___5-7B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_path,  torch_dtype=torch.bfloat16, trust_remote_code=True)

# LoRA 配置
peft_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules="all-linear",  # 根据模型需要调整
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, peft_config)
model = model.to(device)

# 加载数据
def load_data(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]

# dataset = load_data("../data/test.jsonl")
dataset = load_data("../data/FCGEC_train_filtered_modified.jsonl")

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
split = ds.train_test_split(test_size=0.1)
train_ds = split['train']
eval_ds = split['test']


# 配置训练参数
training_args = SFTConfig(
    seed = 42,
    output_dir="../output",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=16,
    learning_rate=5e-5,
    num_train_epochs=1,
    logging_dir='../logs',
    logging_steps=10,
    save_steps=500,
    save_total_limit=2,
    bf16=True,
    report_to="tensorboard",  # 使用 TensorBoard 来报告日志
    logging_first_step=True,
    max_length = 1024,
    max_seq_length = 1024,
    label_names=["labels"],
)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False,
)

# 设置 SFTTrainer
trainer = SFTTrainer(
    model=model,
    train_dataset=train_ds,
    eval_dataset=eval_ds,
    args=training_args,
    data_collator=data_collator,
)

# 启动训练
trainer.train()

# 保存adapter
trainer.model.save_pretrained("../output")