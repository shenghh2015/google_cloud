import os
import multiprocessing
import json
from translate import translate_text
import time
from nlp import pydict_file_read, pydict_file_write
import argparse
from datetime import date
import random

random.seed(0)

# load jsonl data
def load_jsonl(data_path):
    data = []
    with open(data_path) as f:
        prompt_id = 0
        for line in f:
            jdata = json.loads(line)
            jdata['id'] = prompt_id
            prompt_id += 1
            data.append(jdata)
    return data

# google translation
def google_translate(text):
    result = translate_text('zh-CH', text)
    return result['translatedText']

# process one data
def translate_data(prompt_data, index, results, output_path):
    prompt = prompt_data['conversations'][0]['value']
    response = prompt_data['conversations'][1]['value']
    translated_prompt = google_translate(prompt)
    translated_response = google_translate(response)
    convers = [
        {'from': 'human',
        'value': translated_prompt},
        {'from': 'assistant',
        'value': translated_response}
    ]
    result = {
        'id': prompt_data['id'],
        'conversations': convers,
        'split': prompt_data['split']
    }

    if index % 20 == 0:
        pydict_file_write(results, output_path)

    return result

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str, default='.')
    parser.add_argument("--output_dir", type=str, default='.')
    parser.add_argument("--num_workers", type=int, default=8)
    parser.add_argument("--start_id", type=int, default=0)
    parser.add_argument("--end_id", type=int, default=20)
    return parser.parse_args()

# input_path = '/home/paiinlpteam/data/long_examples.pydict'

def main():

    args = get_args()
    pydict_path = args.input_path

    # output path
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)
    dataset_name = 'long_examples_zh'
    uid = 'sft_55'
    today = '{}'.format(date.today())
    output_path = os.path.join(output_dir, f'data.{uid}.{dataset_name}.{today}_s{args.start_id}_e{args.end_id}.pydict')

    pydict_data_ = pydict_file_read(pydict_path)

    # first num_data
    pydict_data = []
    for data in pydict_data_:
        prompt_id = data['id']
        if prompt_id >= args.start_id and prompt_id < args.end_id:
            pydict_data.append(data)
    print(f'prompts to be processed: {len(pydict_data)}')

    results = []
    num_workers = args.num_workers
    with multiprocessing.Pool(num_workers) as pool:
        for index, data in enumerate(pydict_data):
            pool.apply_async(translate_data, args = (data, index, results, output_path), callback = results.append)
        pool.close()
        pool.join()
    results = sorted(results, key = lambda x: x['id'])
    print(f'prompts processed: {len(results)}')
    pydict_file_write(results, output_path)

if __name__ == '__main__':
    main()