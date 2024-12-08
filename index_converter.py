import pickle
import sys
import csv

with open('./index.txt', 'r') as index_txt:
    with open('./index.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        lines = index_txt.readlines()
        data = [line.strip().split() for line in lines]

        writer.writerows(data)
