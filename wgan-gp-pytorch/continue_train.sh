#!/bin/bash 
python train.py --train_dir [train_dir] --validation_dir [val_dir] --output_path [out_dir] --dim 64 --saving_step 300 --num_workers 8 --restore_mode --start_iter [start_iter] --batch_size 32