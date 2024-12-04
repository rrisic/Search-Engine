from nltk.stem.porter import PorterStemmer
from posting import Posting
import math
import time
import pickle

STEMMER = PorterStemmer()
NUM_DOCS = 55393


def process_line(line):
    file_info = line.strip().split(' ')
    if not file_info[0]:
        return None
    key = file_info[0]
    postings = set()
    doc_freq = 0
    pairs = zip(file_info[1::2], file_info[2::2])
    for doc, freq in pairs:
        postings.add(Posting(doc, freq))
        doc_freq += 1
    return key, postings, doc_freq




def query(user_query : str, index, doc_frequencies):
    query_list = user_query.split(" ")
    query_list = [STEMMER.stem(token.lower()) for token in query_list] # need to be stemmed to corresspond with index

        
    response_ids = {} # id : tf-idf score
    
    for i in range(0, len(query_list)):
        if (query_list[i] in index): # should change ordering in future
            for post in index[query_list[i]]:
                tf = post._word_count
                df = doc_frequencies[query_list[i]]
                idf = NUM_DOCS / df
                log_tf = math.log10(tf) + 1
                log_idf = math.log2(idf)
                tf_idf = log_tf * log_idf

                if (post._doc_id in response_ids):
                    response_ids[post._doc_id] += tf_idf
                else:
                    response_ids[post._doc_id] = tf_idf

    return response_ids

def doc_id_reader(response_ids):
    doc_ids = {}

    with open('./doc_ids.txt') as id_file:
        count = 1
        while True:
            cur = id_file.readline()
            if (cur == ''):
                break
            doc_ids[str(count)] = cur
            count += 1

    ret_dict = {}
    for id in response_ids:
        ret_dict[doc_ids[id].strip()] = response_ids[id]

    return ret_dict

if __name__ == '__main__':
    start_time = time.time()
    doc_frequency = {}

    index = {}
    

    

    with open('./index.txt', 'r') as index_file:
        total_file_info = index_file.readlines()
        for file_info in total_file_info:
            file_info = file_info.split(' ')
            if (file_info[0] == ''):
                break
            index[file_info[0]] = set()
            doc_frequency[file_info[0]] = 0
            for i in range(1, len(file_info) - 2, 3):
                index[file_info[0]].add(Posting(file_info[i], file_info[i + 1], file_info[i + 2]))
                doc_frequency[file_info[0]] += 1
    
    
    
        
    end_time = time.time()
    print(f'Time taken to create index: {(end_time - start_time)}')
    print(f'Size of dictionary: {len(index)}')

    while True:
        query_inp = input("Query: ")
        if (not query_inp):
            break

        resp = query(query_inp, index, doc_frequency)
        ret = doc_id_reader(resp)

        sorted_ret = dict(sorted(ret.items(), key=lambda item: item[1]))
        reversed_sorted_ret = reversed(sorted_ret)

        count = 0
        for a in reversed_sorted_ret:
            if (count == 5):
                break
            print(a)
            count += 1


            
