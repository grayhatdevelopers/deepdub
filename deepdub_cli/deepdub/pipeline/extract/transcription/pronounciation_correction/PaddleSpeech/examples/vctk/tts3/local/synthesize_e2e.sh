#!/bin/bash

config_path=$1
train_output_path=$2
ckpt_name=$3

FLAGS_allocator_strategy=naive_best_fit \
FLAGS_fraction_of_gpu_memory_to_use=0.01 \
python3 ${BIN_DIR}/../synthesize_e2e.py \
    --am=fastspeech2_vctk \
    --am_config=${config_path} \
    --am_ckpt=${train_output_path}/checkpoints/${ckpt_name} \
    --am_stat=dump/train/speech_stats.npy \
    --voc=pwgan_vctk \
    --voc_config=pwg_vctk_ckpt_0.1.1/default.yaml  \
    --voc_ckpt=pwg_vctk_ckpt_0.1.1/snapshot_iter_1500000.pdz \
    --voc_stat=pwg_vctk_ckpt_0.1.1/feats_stats.npy \
    --lang=en \
    --text=${BIN_DIR}/../sentences_en.txt \
    --output_dir=${train_output_path}/test_e2e \
    --phones_dict=dump/phone_id_map.txt \
    --speaker_dict=dump/speaker_id_map.txt \
    --spk_id=0
