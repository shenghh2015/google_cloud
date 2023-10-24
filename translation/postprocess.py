from tools.nlp import pydict_file_read, pydict_file_write
import os


class PostProcessing:
  def __init__(self, data_paths=[], processing_fns=[], output_path=None):

    self.data_list = self._collate_data(data_paths)
    self.output_path = output_path
    self.processing_fns = processing_fns

  def _collate_data(self, data_paths):
    _collated_data = []
    for data_path in data_paths:
      _dataset = pydict_file_read(data_path)
      for d in _dataset:
        _collated_data.append(d)
    return _collated_data

  def processing(self):
    _processed_data = self.data_list
    for prc_fn in self.processing_fns:
      _processed_data = prc_fn(_processed_data)
    self.data_list = _processed_data

  def save(self):
    if self.data_list:
      output_dir = os.path.dirname(self.output_path)
      os.makedirs(output_dir, exist_ok=True)
      pydict_file_write(self.data_list, self.output_path)
      print(f'Saved to {self.output_path}!')
