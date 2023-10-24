from nlp import pydict_file_read
import os
import numpy as np

def main():
    data_path = os.path.expanduser('~/results/data.sft_55.long_examples_zh.2023-10-24_s1400_e1600.pydict')
    pydict_data = pydict_file_read(data_path)
    collected_ids = set()
    for data in pydict_data:
        if not data['id'] in collected_ids:
            collected_ids.add(data['id'])
    collected_ids = list(collected_ids)
    min_id, max_id = min(collected_ids), max(collected_ids)
    print(f'collected ids: {len(collected_ids)}')
    print(min_id, max_id)
    missed_ids = []
    for i in range(min_id, max_id + 1):
        if not i in collected_ids:
            missed_ids.append(i)
    print(len(missed_ids))
    np.save(os.path.expanduser('~/data/missed_ids2.npy'), missed_ids)

if __name__ == '__main__':
    main()