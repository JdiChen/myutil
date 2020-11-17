import yaml


def yaml_read(path):
    file_read = {}
    with open(path, 'r', encoding='utf-8') as f:
        file_read = yaml.safe_load(f)
    return file_read


if __name__ == '__main__':
    print(yaml_read('test.yaml'))
