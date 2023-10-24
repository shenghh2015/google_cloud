DATA_DIR=/tmp/2023-10-24.google_translation/results
OUTPUT_DIR=/tmp/2023-10-24.google_translation/final_results
python translation/postprocess_data.py --data_dir $DATA_DIR \
--output_dir $OUTPUT_DIR \
--data_uid sft_55 \
--data_name long_examples_zh \
