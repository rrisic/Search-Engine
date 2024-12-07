from flask import Flask, request, render_template
from posting import Posting
from query_finder import query, doc_id_reader  # Import your search functions

app = Flask(__name__)

# Load the index and doc frequency once
index = {}
doc_frequency = {}
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

@app.route('/', methods=['GET', 'POST'])
def search():
    results = []
    if request.method == 'POST':
        user_query = request.form['query']
        if user_query.strip():
            response_ids = query(user_query, index, doc_frequency)
            results_dict = doc_id_reader(response_ids)
            sorted_results = dict(sorted(results_dict.items(), key=lambda item: item[1], reverse=True))
            results = list(sorted_results.keys())[:5]  # Top 5 results
    return render_template('search.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
