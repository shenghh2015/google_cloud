from postprocess import PostProcessing
import argparse
import os
from datetime import date
import random


def add_ids(datalist):
  _datalist = []
  for i, data in enumerate(datalist):
    data['id'] == i
    _datalist.append(data)
  return _datalist


def random_split(datalist):
  random.seed(0)
  test_ratio = 0.2
  for d in datalist:
    d['split'] = 'train' if random.random() >= test_ratio else 'tset'
  return datalist


def sorted_fn(datalist):
  return sorted(datalist, key=lambda x: x['id'])


def remove_redundant(datalist):
  id_cache = set()
  _datalist = []
  for d in datalist:
    if not d['id'] in id_cache:
      _datalist.append(d)
      id_cache.add(d['id'])
  return _datalist


def data_analysis(datalist):

  if not datalist: return datalist

  exist_ids = []
  for d in datalist:
    exist_ids.append(int(d['id']))
  min_id, max_id = min(exist_ids), max(exist_ids)
  missed_ids = [i for i in range(min_id, max_id + 1) if not i in exist_ids]

  print(f'Id Range: [{min_id}, {max_id})')
  if len(missed_ids) < 20:
    print(f'Missed Ids: {missed_ids}')
  else:
    print(f'Missed Id count: {len(missed_ids)}')
  return datalist


def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("--data_dir", type=str, default=None)
  parser.add_argument("--output_dir", type=str, default='/tmp')
  parser.add_argument("--data_uid", type=str, default='/tmp')
  parser.add_argument("--data_name", type=str, default='/tmp')
  return parser.parse_args()


def main():

  args = get_args()

  data_paths = [
      os.path.join(args.data_dir, n) for n in os.listdir(args.data_dir)
      if n.endswith('.pydict')
  ]
  processing_fns = [remove_redundant, sorted_fn, data_analysis]
  today = '{}'.format(date.today())
  output_name = f'data.{args.data_uid}.{args.data_name}.{today}.pydict'
  output_path = os.path.join(args.output_dir, output_name)
  data_postprocess = PostProcessing(data_paths=data_paths,
                                    processing_fns=processing_fns,
                                    output_path=output_path)
  data_postprocess.processing()
  data_postprocess.save()


if __name__ == '__main__':
  main()
