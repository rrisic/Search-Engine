from nltk.stem.porter import PorterStemmer
from posting import Posting
STEMMER = PorterStemmer()


def query(user_query : str, index):
    query_list = user_query.split(" ")
    query_list = [STEMMER.stem(token.lower()) for token in query_list] # need to be stemmed to corresspond with index

        
    response_ids = set()
    if (query_list):
        if (query_list[0] in index): # should change ordering in future
            for post in index[query_list[0]]:
                response_ids.add(post._doc_id)
    
    
    for i in range(0, len(query_list)):
        if (not response_ids):
            break
        temp_ids = set()
        if (query_list[i] in index): # should change ordering in future
            for post in index[query_list[i]]:
                temp_ids.add(post._doc_id)
        
            response_ids &= temp_ids

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

    ret_set = set()
    for id in response_ids:
        ret_set.add(doc_ids[id].strip())

    return ret_set

if __name__ == '__main__':
    print(STEMMER.stem("ACM"))
    index = {}
    with open('./index.txt') as index_file:
        while True:
            file_info = index_file.readline().split(' ')
            if (file_info[0] == ''):
                break
            index[file_info[0]] = set()
            for i in range(1, len(file_info) - 1, 2):
                index[file_info[0]].add(Posting(file_info[i], file_info[i + 1]))

    while True:
        query_inp = input("Query: ")
        if (not query_inp):
            break

        resp = query(query_inp, index)
        ret = doc_id_reader(resp)

        count = 0
        for a in ret:
            if (count == 5):
                break
            print(a)
            count += 1

            
