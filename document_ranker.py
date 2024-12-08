import numpy as np


# NOT FUNCTIONAL -- CONSUMES TOO MUCH MEMORY

THRESHOLD = 0.1 # chance of jumping to a random page
NUM_DOCS = 55393

def inverse_doc_id_reader(links):
    doc_ids = {}

    with open('./doc_ids.txt') as id_file:
        count = 1
        while True:
            cur = id_file.readline()
            if (cur == ''):
                break
            doc_ids[cur] = str(count)
            count += 1
        num_files = count
    
    ret = [0 for _ in range(num_files)]
    for link in links:
        if (link in doc_ids):
            ret[doc_ids[link] - 1] = 1
    
    return ret

    


def main():
    page_rank_matrix = []
    with open('./link_storage.txt') as file:
        count = 0
        while True:
            print(count)
            count += 1
            line = file.readline()
            if not line:
                break
            line = line.strip().split(' ')
            page_rank_matrix.append(inverse_doc_id_reader(line))
    

    alpha = THRESHOLD
    L = np.array(page_rank_matrix)
    m = np.shape(L)[0]  # number of websites (nodes)

    # Create the state transition matrix T
    T = L.copy()
    for i in range(m):
        s = np.sum(T[i])
        # Normalize by the number of outgoing links to create transition probabilities
        if (s == 0):
            T[i, i] = 1 # For websites with no outgoing links, set T[i,i]=1
        
        else:
            T[i] *= (1 / s)
            

    
    B = L.copy()
    
    for i in range(m):
        for j in range(len(L[i])):
            B[i, j] = 1 / m
    

    G = ((1 - alpha) * T) + (alpha * B)

    n = 1000 # number of page jumps 
    m = np.shape(G)[0]

    pi = np.ones(m) / m
    # diff = np.zeros(n)

    for i in range(n):
        print(i)
        newpi = pi @ G

        # diff[i] = abs(np.sum((newpi - pi)))

        pi = newpi
    
    with open('./rankings.txt', 'w') as file:
        for val in pi:
            file.write(f'{str(val)}\n')


if __name__ == '__main__':
    main()