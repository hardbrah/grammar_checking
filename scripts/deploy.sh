#!/bin/bash
export VLLM_DEVICE=cuda

# export VLLM_LOGGING_LEVEL=DEBUG
vllm serve /mnt/workspace/.cache/modelscope/models/Qwen/Qwen2___5-7B-Instruct \
    --dtype bfloat16 \
    --lora-dtype bfloat16 \
    --gpu-memory-utilization 0.8 \
    --max-num-seqs 1 \
    --max-model-len 1024 \
    --enable-lora \
    --device cuda \
    --lora-modules '{"name":"grammar_checking", "path": "/mnt/workspace/grammar_checking/output/checkpoint-1076"}'