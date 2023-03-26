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
    {'name': 'Data Structures and Algorithms 2', 'level': '1', 'catalog_number': 'CS3100', 'class_number': '1', 'subject': 'Computer Science', 'description': 'This course is a continuation of CS 2100. It covers the design and analysis of algorithms, including sorting, searching, and graph algorithms. It also covers the design and analysis of data structures, including lists, trees, and hash tables. The course also covers the design and analysis of algorithms for solving problems in the real world, including dynamic programming, greedy algorithms, and divide-and-conquer algorithms. The course also covers the design and analysis of algorithms for solving problems in the real world, including dynamic programming, greedy algorithms, and divide-and-conquer algorithms.'},
    {'name': 'Introduction to Sociology', 'level': '1', 'catalog_number': 'STS1500', 'class_number': '1', 'subject': 'Sociology', 'description': 'This course is an introduction to the sociological study of human behavior. It covers the basic concepts and theories of sociology, including socialization, culture, social structure, social interaction, and social change. It also covers the basic concepts and theories of sociology, including socialization, culture, social structure, social interaction, and social change.'}
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