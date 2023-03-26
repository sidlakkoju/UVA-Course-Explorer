from flask import Flask, jsonify, request
import time
from openai.embeddings_utils import get_embedding, cosine_similarity
import pandas as pd
from config import openai_key
import openai
import numpy as np
from semantic_search import *
import threading
import requests

openai.api_key = openai_key


# Test Return array
test_return_array = [
    {'name': 'Data Structures and Algorithms 2', 'level': '1', 'catalog_number': 'CS3100', 'class_number': '1', 'subject': 'Computer Science', 'description': 'This course is a continuation of CS 2100. It covers the design and analysis of algorithms, including sorting, searching, and graph algorithms. It also covers the design and analysis of data structures, including lists, trees, and hash tables. The course also covers the design and analysis of algorithms for solving problems in the real world, including dynamic programming, greedy algorithms, and divide-and-conquer algorithms. The course also covers the design and analysis of algorithms for solving problems in the real world, including dynamic programming, greedy algorithms, and divide-and-conquer algorithms.'},
    {'name': 'Introduction to Sociology', 'level': '1', 'catalog_number': 'STS1500', 'class_number': '1', 'subject': 'Sociology', 'description': 'This course is an introduction to the sociological study of human behavior. It covers the basic concepts and theories of sociology, including socialization, culture, social structure, social interaction, and social change. It also covers the basic concepts and theories of sociology, including socialization, culture, social structure, social interaction, and social change.'}
]


detailed_info = {}

app = Flask(__name__)



# class for query builder?
def get_base_url(year=2023, term="spring"):
    year_str = str(year)[-2:]
    term_num = 8
    if term == "spring":
        term_num = 2
    
    return f"https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1{year_str}{term_num}"




def get_detailed_info_url(catalog_nbr, subject, year=2023, term="spring"):
    base_url = get_base_url(year, term)
    return f"{base_url}&subject={subject}&catlog_nbr={catalog_nbr}"



# Test route
@app.route('/members')
def get_members():
    return {'members': ['John', 'Paul', 'George', 'Ringo']}




def get_detailed_info(json_results):
    global detailed_info
    for i in range(len(json_results)):
        catalog_nbr = json_results[i]['catalog_nbr']
        subject = json_results[i]['subject']



        detailed_info_url = get_detailed_info_url(catalog_nbr, subject)
        r = requests.get(detailed_info_url)
        array = r.json()

        print(array)


@app.route('/search', methods=['POST'])
def search():
    search_input = request.json['searchInput']
    json_results = get_top_results_json(search_input, n=10)

    t = threading.Thread(target=get_detailed_info, args=(json_results,))
    t.start()
    t.join()
    return json_results


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

    #new_search_results = jsonify(test_return_array)