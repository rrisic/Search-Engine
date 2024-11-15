from posting import Posting
import json
import os

# JSON format : 
# url:
# content:
# encoding:

DEV_DIR = './DEV'
SESSION_LIMIT = 1000

def main():
    count = 0  # Used to store documentIDs
    session_count = 0 # Used to clear local program memory when needed
    for directory in os.listdir(DEV_DIR):
        dir = os.path.join(DEV_DIR, directory)
        for filename in os.listdir(dir):
            file = os.path.join(dir, filename)
            count += 1
            session_count += 1
            with open(file, 'r') as open_json:
                data = json.load(open_json)



