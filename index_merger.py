from posting import Posting

NUM_FILES = 5
'''
def main():
    with open('./PartialIndexes/1.txt', 'r') as file1, open(f'./PartialIndexes/2.txt') as file2:
        file1_dict = {}
        while True:
            file1_info = file1.readline().split(' ')
            if (file1_info[0] == ''):
                break
            file1_dict[file1_info[0]] = set()
            for i in range(1, len(file1_info) - 2, 3):
                file1_dict[file1_info[0]].add(Posting(file1_info[i], file1_info[i + 1], file1_info[i + 2]))
        file2_dict = {}
        while True:
            file2_info = file2.readline().split(' ')
            if (file2_info[0] == ''):
                break
            file2_dict[file2_info[0]] = set()
            for i in range(1, len(file2_info) - 2, 3):
                file2_dict[file2_info[0]].add(Posting(file2_info[i], file2_info[i + 1], file2_info[i + 2]))
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
                for i in range(1, len(file1_info) - 2, 3):
                    file1_dict[file1_info[0]].add(Posting(file1_info[i], file1_info[i + 1], file1_info[i + 2]))
        for key in file1_dict:
            if key not in file2_dict:
                file2_dict[key] = set()
            for posting in file1_dict[key]:
                file2_dict[key].add(posting)
    
    with open('./index.txt', 'w') as PIfile:
        for key in file2_dict:
            PIfile.write(f'{key} ')
            for posting in file2_dict[key]:
                PIfile.write(f'{posting._doc_id} {posting._word_count} {posting._word_count} ')
            PIfile.write('\n')'''

def main():
    for i in range(1, NUM_FILES + 1):
        with open(f'./PartialIndexes/{i}.txt') as file:
            while True:
                line = file.readline()
                if (not line):
                    break
                line_list = line.split(' ')
                with open(f'./Indexes/{line[0]}.txt', 'a') as letter_file:
                    letter_file.write(f'{line_list[0]} ')
                    for i in range(1, len(line_list) - 2, 3):
                        letter_file.write(f'{line_list[i]} {line_list[i+1]} {line_list[i+2]} ')
                    letter_file.write('\n')
                    letter_file.flush()

    offsets = {}
    for char in "abcdefghijklmnopqrstuvwxyz0123456789":
        index = {}
        with open(f'./Indexes/{char}.txt', 'r') as index_file:
            total_file_info = index_file.readlines()
            for file_info in total_file_info:
                file_info = file_info.strip().split(' ')
                if (file_info[0] == ''):
                    break
                if file_info[0] not in index:
                    index[file_info[0]] = set()
                for i in range(1, len(file_info) - 2, 3):
                    index[file_info[0]].add(Posting(file_info[i], file_info[i + 1], file_info[i + 2]))
        
        with open(f'./Indexes/{char}.txt', 'w') as file:
            for key in sorted(index):
                file.write(f'{key} ')
                for posting in index[key]:
                    file.write(f'{posting._doc_id} {posting._word_count} {int(posting._is_special)} ')
                file.write('\n')
        
        with open(f'./Indexes/{char}.txt', 'rb') as file:
            while True:
                cur = file.tell()
                line = file.readline()
                if not line:
                    break
                word = line.decode('utf-8').strip().split(' ')[0]
                offsets[word] = cur


    with open('./offsets.txt', 'w') as file:
        for key in offsets:
            file.write(f'{key} {offsets[key]}\n')
    

            


    






if __name__ == '__main__':
    main()