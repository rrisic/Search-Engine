import os
from bs4 import BeautifulSoup
import json

DEV_DIR = './DEV'

def main():
    with open("./doc_ids.txt", 'w') as doc_id_file:
        for directory in os.listdir(DEV_DIR):
            dir = os.path.join(DEV_DIR, directory)
            if (os.path.isfile(dir)):
                continue
            for filename in os.listdir(dir):
                file = os.path.join(dir, filename)
                with open(file, 'r') as open_json:
                    data = json.load(open_json)
                    doc_id_file.write(data['url'])
                    doc_id_file.write('\n')
            


if __name__ == '__main__':
    main()