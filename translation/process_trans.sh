# run translation for data with id range: [start_id, end_id)
INPUT_PATH=/tmp/2023-10-24.google_translation/data.sft_54.long_examples_en.2023-10-24.pydict
ID_REF_PATH=/tmp/2023-10-24.google_translation/data.sft_55.long_examples_zh.2023-10-24_s700_e1400.pydict
python translation/process_trans.py --input_path $INPUT_PATH \
--output_dir /tmp/results \
--start_id 0 \
--end_id 100 \
--id_ref_path None \
--data_uid sft_56 \
--data_name long_examples_en_test \

# run translation for data with id_ref_path
python translation/process_trans.py --input_path $INPUT_PATH \
--output_dir /tmp/results \
--start_id -1 \
--end_id -1 \
--id_ref_path $ID_REF_PATH \
--data_uid sft_56 \
--data_name long_examples_en_test \

# run translation for data with known_ids
python translation/process_trans.py --input_path $INPUT_PATH \
--output_dir /tmp/results \
--known_ids 100,101,102,103 \
--data_uid sft_56 \
--data_name long_examples_en_test \