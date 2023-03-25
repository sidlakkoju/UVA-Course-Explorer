from flask import Flask, jsonify, request
import time


# Test Return array
test_return_array = [
    {'name': 'CS3100', 'description': 'Course about DSA2'},
    {'name': 'STS1500', 'description': 'thats a great question'}
]

app = Flask(__name__)


# Test route
@app.route('/members')
def get_members():
    return {'members': ['John', 'Paul', 'George', 'Ringo']}



@app.route('/search', methods=['POST'])
def search():
    search_input = request.json['searchInput']
    # Perform search based on search_input

    '''
    search_results = [search_input + ' Results: ', 'Result 1', 'Result 2', 'Result 3'] # Replace with your actual search code
    return jsonify({'results': search_results})
    '''

    return jsonify(test_return_array)

    #new_search_results = jsonify(test_return_array)