from posting import Posting
import json
import os
import nltk
from bs4 import BeautifulSoup
from nltk.stem.porter import PorterStemmer

# JSON format : 
# url:
# content:
# encoding:

DEV_DIR = './DEV'
SESSION_LIMIT = 1000


def main():
    count = 0  # Used to store documentIDs
    session_count = 0 # Used to clear local program memory when needed
    file_name_counter = 0
    partial_index = {}
    doc_ids = {}
    for directory in os.listdir(DEV_DIR):
        dir = os.path.join(DEV_DIR, directory)
        if (os.path.isfile(dir)):
            continue
        for filename in os.listdir(dir):
            file = os.path.join(dir, filename)
            count += 1
            session_count += 1
            if (session_count == SESSION_LIMIT):
                file_name_counter += 1
                with open(f'./PartialIndexes/{file_name_counter}.txt', 'w') as PIfile:
                    for key in partial_index:
                        PIfile.write(f'{key} ')
                        for posting in partial_index[key]:
                            PIfile.write(f'{posting._doc_id} {posting._word_count} ')
                        PIfile.write('\n')
                session_count = 0
                partial_index={}
            with open(file, 'r') as open_json:
                stemmer = PorterStemmer()
                data = json.load(open_json)
                soup = BeautifulSoup(data['content'], 'html.parser')
                text = soup.get_text()
                doc_ids[count] = data['url']
                tokens = nltk.tokenize.RegexpTokenizer(r"[A-Za-z0-9']+").tokenize(text.lower()) # Purposefully includes apostrophe
                stemmed_tokens = [stemmer.stem(token) for token in tokens]
                stemmed_tokens_dict = word_count_dict(stemmed_tokens)
                for token in stemmed_tokens_dict:
                    if token in partial_index:
                        partial_index[token].add(Posting(count, stemmed_tokens_dict[token]))
                    else:
                        newPost = Posting(count, stemmed_tokens_dict[token])
                        partial_index[token] = set()
                        partial_index[token].add(newPost)
    file_name_counter += 1
    with open(f'./PartialIndexes/{file_name_counter}.txt', 'w') as PIfile:
        for key in partial_index:
            PIfile.write(f'{key} ')
            for posting in partial_index[key]:
                PIfile.write(f'{posting._doc_id} {posting._word_count} ')
            PIfile.write('\n')
    with open('./doc_ids.txt', 'a') as file:
        for key in doc_ids:
            file.write(f'{doc_ids[key]}\n')
    print(count)

def word_count_dict(tokens):
    dict = {}
    for token in tokens:
        if token in dict:
            dict[token] += 1
        else:
            dict[token] = 1
    return dict


if __name__ == '__main__':
    main()



            




