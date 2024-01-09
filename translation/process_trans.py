from translate import google_translate
from datasets import Dataset, DataLoader
from translator import Translator
from tools.nlp import pydict_file_write
import argparse
from datetime import date
import os

# google translation flag
# GOOGLE_TRANSLATION = False
GOOGLE_TRANSLATION = True

# translate function
def translate_fn(data):
  prompt = data['conversations'][0]['value']
  response = data['conversations'][1]['value']
  if GOOGLE_TRANSLATION:
    translated_prompt = google_translate(prompt)
    translated_response = google_translate(response)
  else:
    translated_prompt = prompt
    translated_response = response
  data['conversations'][0]['value'] = translated_prompt
  data['conversations'][1]['value'] = translated_response
  print('translate {}'.format(data['id']))
  return data


# save function
def save_fn(outputs, output_path):
  pydict_file_write(outputs, output_path)


def get_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("--input_path", type=str, default=None)
  parser.add_argument("--output_dir", type=str, default='/tmp')
  parser.add_argument("--start_id", type=int, default=-1)
  parser.add_argument("--end_id", type=int, default=-1)
  parser.add_argument("--id_ref_path", type=str, default=None)
  parser.add_argument("--known_ids", type=str, default=None)
  parser.add_argument("--data_uid", type=str, default=None)
  parser.add_argument("--data_name", type=str, default=None)
  return parser.parse_args()


def main():

  # parameters
  args = get_args()

  # output path
  today = '{}'.format(date.today())
  output_name = f'data.{args.data_uid}.{args.data_name}.{today}.pydict'
  if args.end_id > args.start_id:
    output_name = output_name.replace(
        '.pydict', f'_s{args.start_id}_e{args.end_id}.pydict')
  elif args.id_ref_path is not None:
    output_name = os.path.basename(args.input_path)
    output_name = output_name.replace('.pydict', f'_missed.pydict')
  elif args.known_ids:
    output_name = output_name.replace('.pydict', f'_kwn_ids.pydict')
  output_path = os.path.join(args.output_dir, output_name)

  # dataset
  known_ids = [int(i)
               for i in args.known_ids.split(',')] if args.known_ids else []
  dataset = Dataset(args.input_path, args.start_id, args.end_id,
                    args.id_ref_path, known_ids)
  dataloader = DataLoader(dataset, collate_fn=lambda x: x)

  # translation
  translator = Translator(dataloader=dataloader,
                          translate_fn=translate_fn,
                          save_fn=save_fn,
                          output_path=output_path)
  translator.translate()

  # save translation results
  translator.save(sorting=True)


if __name__ == '__main__':
  main()
