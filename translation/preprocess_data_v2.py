from tools.nlp import pydict_file_write
import json
from datetime import date
import os
import random
import numpy as np

random.seed(0)

# load jsonl data
def load_jsonl(data_path):
  pydict_data = []
  with open(data_path) as f:
    prompt_id = 0
    for line in f:
      jdata = json.loads(line)
      prompt_id += 1
      convers = [{
          'from': 'human',
          'value': jdata['instruction']
      }, {
          'from': 'assistant',
          'value': jdata['output']
      }]
      data = {
          'id': prompt_id,
          'conversations': convers,
          'split': 'train' if random.random() > 0.2 else 'test'
      }
      pydict_data.append(data)
  return pydict_data

def load_json(data_path):
  output_data = []
  with open(data_path) as f:
    json_data = json.load(f)
    for i, jdata in enumerate(json_data):
      data = {
        'id': i,
        'conversations': jdata['conversations'],
        'idx': jdata['idx'],
        'split': 'train' if random.random() > 0.2 else 'test'
      }
      # data['conversations'][1]['from'] = 'assistant'
      for c in data['conversations']:
        if c['from'] == 'gpt': c['from'] = 'assistant'
      output_data.append(data)
  print(f'Number of data: {len(output_data)}')
  return output_data

def analyze_translation_cost(data):
  char_count = 0
  prompt_count = 0
  for d in data:
    prompt_count += 1
    for c in d['conversations']:
      char_count += len(c['value'])
  char_count_in_million = round(char_count / 1e6, 4)
  price = 20
  cost = round(price * char_count_in_million, 4)
  print(f"total character count: {char_count}")
  print(f"total charcter count (Millions): {char_count_in_million}")
  print(f"total cost: {cost}$")
  return char_count

def get_start_and_end_by_cost(data, cost_thresh = 2000):
  char_count = 0
  prompt_count = 0
  price = 20
  for d in data:
    prompt_count += 1
    for c in d['conversations']:
      char_count += len(c['value'])
    char_count_in_million = round(char_count / 1e6, 4)
    cost = round(price * char_count_in_million, 4)
    if cost > cost_thresh: break
  print("**************************")
  print(f"Translation of {prompt_count} prompts costs ${cost_thresh}")
  print(f"character count: {char_count}")
  print(f"charcter count (Millions): {char_count_in_million}")
  print(f"final cost: {cost}$")
  print("**************************")
  return char_count

def analyze_data(data):
  train_num = 0
  test_num = 0
  turns_num = []
  for d in data:
    train_num += d['split'] == 'train'
    test_num += d['split'] == 'test'
    turns_num.append(len(d['conversations']))
  print(f'train data: {train_num}, test data: {test_num}')
  print(f'turn statistics: mean {np.mean(turns_num)}, std {np.std(turns_num)}')

def main():
  data_path = os.path.expanduser('~/data/WizardLM_evol_instruct_V2_143k.json')
  pydict_data = load_json(data_path)

  # analze cost
  analyze_translation_cost(pydict_data)
  
  # get start and end ids
  get_start_and_end_by_cost(pydict_data, cost_thresh = 2000)
  
  # analyze train/test
  analyze_data(pydict_data)
  
  output_dir = os.path.expanduser('~/data')
  os.makedirs(output_dir, exist_ok=True)
  dataset_name = 'WizardLM_evol_instruct_en'
  uid = 'sft_60'
  today = '{}'.format(date.today())
  output_path = os.path.join(output_dir,
                             f'data.{uid}.{dataset_name}.{today}.pydict')
  pydict_file_write(pydict_data, output_path)


if __name__ == '__main__':
  main()
