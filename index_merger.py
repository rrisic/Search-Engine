from posting import Posting

NUM_FILES = 56
def main():
    with open('./PartialIndexes/1.txt', 'r') as file1, open(f'./PartialIndexes/2.txt') as file2:
        file1_dict = {}
        while True:
            file1_info = file1.readline().split(' ')
            if (file1_info[0] == ''):
                break
            file1_dict[file1_info[0]] = set()
            for i in range(1, len(file1_info) - 1, 2):
                file1_dict[file1_info[0]].add(Posting(file1_info[i], file1_info[i + 1]))
        file2_dict = {}
        while True:
            file2_info = file2.readline().split(' ')
            if (file2_info[0] == ''):
                break
            file2_dict[file2_info[0]] = set()
            for i in range(1, len(file2_info) - 1, 2):
                file2_dict[file2_info[0]].add(Posting(file2_info[i], file2_info[i + 1]))
    for key in file1_dict:
        if key not in file2_dict:
            file2_dict[key] = set()
        for posting in file1_dict[key]:
            file2_dict[key].add(posting)
    
    count = 2
    while (count < NUM_FILES):
        count += 1
        with open(f'./PartialIndexes/{count}.txt') as file1:
            file1_dict = {}
            while True:
                file1_info = file1.readline().split(' ')
                if (file1_info[0] == ''):
                    break
                file1_dict[file1_info[0]] = set()
                for i in range(1, len(file1_info) - 1, 2):
                    file1_dict[file1_info[0]].add(Posting(file1_info[i], file1_info[i + 1]))
        for key in file1_dict:
            if key not in file2_dict:
                file2_dict[key] = set()
            for posting in file1_dict[key]:
                file2_dict[key].add(posting)
    
    with open('./index.txt', 'w') as PIfile:
        for key in file2_dict:
            PIfile.write(f'{key} ')
            for posting in file2_dict[key]:
                PIfile.write(f'{posting._doc_id} {posting._word_count} ')
            PIfile.write('\n')

    




if __name__ == '__main__':
    main()