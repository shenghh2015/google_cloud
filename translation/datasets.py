from tools.nlp import pydict_file_read

class Dataset:
    def __init__(self, data_path, 
                start_id=-1, end_id=-1, id_ref_path=None, 
                known_ids=[]):
        self.data_iter = pydict_file_read(data_path)
        self.data_iter = self._clip_dataset(self.data_iter, start_id, end_id, id_ref_path, known_ids)

    def _clip_dataset(self, data, start_id=-1, end_id=-1, id_ref_path=None, 
                known_ids=[]):
        _data = []
        _ids = []
        _use_clip = False
        if start_id >=0 and end_id > start_id:
            _ids = [i for i in range(start_id, end_id)]
            _use_clip = True
        elif id_ref_path is not None:
            if id_ref_path.endswith('.npy'):
                import numpy as np
                _ids = np.load(id_ref_path).tolist()
            elif id_ref_path.endswith('.pydict'):
                _id_pydict_data = pydict_file_read(id_ref_path)
                _exist_ids = [int(d['id']) for d in _id_pydict_data]
                print(f'min id {min(_exist_ids)}, max id {max(_exist_ids)}')
                _ids = [i for i in range(min(_exist_ids), max(_exist_ids) + 1) if not i in _exist_ids]
            _use_clip = True
        elif known_ids:
            _ids = known_ids
            _use_clip = True
        if _use_clip:
            _data = [d for d in data if int(d['id']) in _ids]
        else:
            _data = [d for d in data]
        return _data

class DataLoader:
    def __init__(self, dataset, collate_fn=None):
        self.dataset = dataset
        self.collate_fn = collate_fn
    
    def __iter__(self):
        for data in self.dataset.data_iter:
            data = self.collate_fn(data)
            yield data
