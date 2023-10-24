import os


class Translator:
  def __init__(self,
               dataloader=None,
               translate_fn=None,
               save_fn=None,
               output_path=None):
    self.dataloader = dataloader
    self.translate_fn = translate_fn
    self.save_fn = save_fn
    self.output_path = output_path
    self.outputs = None

  def translate(
      self,
      num_worker=1,
  ):
    results = []
    if self.dataloader is not None:
      for data in self.dataloader:
        results.append(self.translate_fn(data))
        if len(results) % 100 == 0:
          self.save()
    self.outputs = results

  def save(self, sorting=False):
    if self.outputs and self.output_path is not None:
      output_dir = os.path.dirname(self.output_path)
      os.makedirs(output_dir, exist_ok=True)
      if sorting:
        self.outputs = sorted(self.outputs, key=lambda x: x['id'])
      self.save_fn(self.outputs, self.output_path)
      print(f'saved to {self.output_path}')
