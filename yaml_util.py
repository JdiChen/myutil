import yaml


def yaml_read(path):
    file_read = {}
    with open(path, 'r', encoding='utf-8') as f:
        file_read = yaml.safe_load(f)
    return file_read

def a(wordtext:str):
    words = wordtext.strip().split(" ")
    return set(words)
if __name__ == '__main__':
    print(a(" a a b c c "))

if __name__ == '__main__':
    print(yaml_read('test.yaml'))
