from tools.nlp import pydict_file_write
import json
from datetime import date
import os
import random

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


def main():
  data_path = os.path.expanduser('~/data/long_examples.jsonl')
  pydict_data = load_jsonl(data_path)

  output_dir = os.path.expanduser('~/data')
  os.makedirs(output_dir, exist_ok=True)
  dataset_name = 'long_examples_en'
  uid = 'sft_54'
  today = '{}'.format(date.today())
  output_path = os.path.join(output_dir,
                             f'data.{uid}.{dataset_name}.{today}.pydict')
  pydict_file_write(pydict_data, output_path)


if __name__ == '__main__':
  main()
