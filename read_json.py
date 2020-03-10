import json

def get_config(name):
    data = {}
    with open(f'{name}.json', 'r') as read_file:
        data = json.load(read_file)
    return data


if __name__ == '__main__':
    print(get_config('config').get('users').get('end'))