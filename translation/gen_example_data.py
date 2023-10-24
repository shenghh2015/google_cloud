from nlp import pydict_file_write

def gen_data(num_data=100):
    result = []
    for i in range(num_data):
        result.append({
            'instruction': 'hello',
            'output': 'world'
        }
        )
    return result

def main():
    output_path = '/home/paiinlpteam/data/example_data.pydict'
    pydict_data = gen_data(400)
    pydict_file_write(pydict_data, output_path)

if __name__ == '__main__':
    main()