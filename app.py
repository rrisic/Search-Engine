from flask import Flask, request, render_template
from posting import Posting
from query_finder import query, doc_id_reader  # Import your search functions
import time

app = Flask(__name__)

# Load the index and doc frequency once
index = {}
doc_frequency = {}
offsets = {}
with open('./offsets.txt', 'r') as file:
    while True:
        line = file.readline()
        if not line:
            break
        line = line.strip().split(' ')
        offsets[line[0]] = line[1]


@app.route('/', methods=['GET', 'POST'])
def search():
    start_time = time.time()
    results = []
    offset = int(request.args.get('offset', 0))  # Read offset from query parameters
    user_query = request.args.get('q', '')  # Get the search query from URL

    # Handle POST logic
    if request.method == 'POST':
        user_query = request.form['query']
        if user_query.strip():
            if len(user_query) > 15:
                query_list = user_query.split(' ')
                if len(query_list) > 5:
                    user_query = ' '.join(query_list[:3])
            response_ids = query(user_query, offsets)
            results_dict = doc_id_reader(response_ids)
            sorted_results = dict(sorted(results_dict.items(), key=lambda item: item[1], reverse=True))
            results = list(sorted_results.keys())
    else:
        # Handle GET logic if there's an offset query
        if user_query.strip():
            response_ids = query(user_query, offsets)
            results_dict = doc_id_reader(response_ids)
            sorted_results = dict(sorted(results_dict.items(), key=lambda item: item[1], reverse=True))
            results = list(sorted_results.keys())

    # Paginate results
    paginated_results = results[offset:offset + 10]
    has_next = offset + 10 < len(results)  # If there are more results available
    has_previous = offset > 0  # If we're past the first set of results

    end_time = time.time()
    message = f"Found {len(results)} relevant pages in {(end_time - start_time) * 1000 // 1} milliseconds"

    return render_template(
        'search.html',
        results=paginated_results,
        message=message,
        offset=offset,
        has_next=has_next,
        has_previous=has_previous,
        user_query=user_query
    )
if __name__ == '__main__':
    app.run(debug=True)
