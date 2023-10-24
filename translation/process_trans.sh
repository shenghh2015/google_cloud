# run translation for data with id range: [start_id, end_id)
python translation/process_trans.py --input_path /home/$USER/data/data.sft_54.long_examples_en.2023-10-24.pydict \
--output_dir /tmp/results \
--start_id 0 \
--end_id 100 \
--id_ref_path None \
--data_uid sft_56 \
--data_name long_examples_en_test \

# run translation for data with id_ref_path
python translation/process_trans.py --input_path /home/$USER/data/data.sft_54.long_examples_en.2023-10-24.pydict \
--output_dir /tmp/results \
--start_id -1 \
--end_id -1 \
--id_ref_path /home/$USER/results/data.sft_55.long_examples_zh.2023-10-24_s700_e1400.pydict \
--data_uid sft_56 \
--data_name long_examples_en_test \

# run translation for data with known_ids
python translation/process_trans.py --input_path /home/$USER/data/data.sft_54.long_examples_en.2023-10-24.pydict \
--output_dir /tmp/results \
--known_ids 100,101,102,103 \
--data_uid sft_56 \
--data_name long_examples_en_test \

