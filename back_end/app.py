from flask import Flask, jsonify, request
import time
from openai.embeddings_utils import get_embedding, cosine_similarity
import pandas as pd
from config import openai_key
import openai
import numpy as np
from semantic_search import *

openai.api_key = openai_key


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
    json_results = get_top_results_json(search_input, n=10)
    return json_results


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

    #new_search_results = jsonify(test_return_array)