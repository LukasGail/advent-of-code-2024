import os

def load_data(file_name):
    input_path = os.path.join(os.path.dirname(__file__), f'../inputs/{file_name}')
    with open(input_path, 'r') as file:
        data = file.read()
    return data