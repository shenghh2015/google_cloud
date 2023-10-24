# python translation/process_data.py --input_path /home/$USER/data/example_data.pydict \
#                                    --output_dir /home/$USER/results \
#                                    --num_workers 3 --num_data 200

# python translation/process_data.py --input_path /home/$USER/data/long_examples.pydict \
#                                    --output_dir /home/$USER/results \
#                                    --num_workers 2 --num_data 20

# python translation/process_data_v2.py --input_path /home/$USER/data/data.sft_54.long_examples_en.2023-10-24.pydict \
#                                    --output_dir /home/$USER/results \
#                                    --num_workers 8 --start_id 0 --end_id 100

# python translation/process_data_v2.py --input_path /home/$USER/data/data.sft_54.long_examples_en.2023-10-24.pydict \
#                                    --output_dir /home/$USER/results \
#                                    --num_workers 2 --start_id 600 --end_id 700

python translation/process_data_v2.py --input_path /home/$USER/data/data.sft_54.long_examples_en.2023-10-24.pydict \
                                   --output_dir /home/$USER/results \
                                   --num_workers 1 --start_id 1569 --end_id 1600