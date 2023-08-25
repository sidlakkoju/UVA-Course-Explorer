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
import json
from datetime import datetime


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
    return f"{base_url}&catlog_nbr={catalog_nbr}&subject={subject}"


# Test route
@app.route('/members')
def get_members():
    return {'members': ['John', 'Paul', 'George', 'Ringo']}


# time_string = "11.00.00.000000-05:00"
def parse_time(time_string, time_format = '%H.%M.%S.%f%z'):
    parsed_time = datetime.strptime(time_string, time_format)
    hours_minutes = f"{parsed_time.hour:02d}:{parsed_time.minute:02d}"
    return  hours_minutes



def populate_detailed_info(json_results):
    global detailed_info
    json_results = json.loads(json_results)
    for i in range(len(json_results)):      # for each search result
        catalog_nbr = str(json_results[i]['catalog_number'])
        subject_mnemonic = str(json_results[i]['mnemonic'])
        detailed_info_url = get_detailed_info_url(catalog_nbr, subject_mnemonic)
        r = requests.get(detailed_info_url)
        array = r.json()
        detailed_info_array = []
        print("Getting data for " + subject_mnemonic + " " + str(catalog_nbr))

        for session in array:       # for each meeting session of the class we're looking at
            # need to filter out results cuz SIS API is sometimes weird
            if str(session['subject']) != subject_mnemonic or str(session['catalog_nbr']) != catalog_nbr:
                continue

            session_data = {}
            try:
                session_data['instructor'] = session['instructors'][0]['name']
            except:
                session_data['instructor'] = "N/A"

            try:
                session_data['type'] = session['component']
            except:
                session_data['type'] = "N/A"

            try:
                session_data['location'] = session['meetings'][0]['facility_descr']
            except:
                session_data['location'] = "N/A"
            
            try:
                session_data['enrollment_capacity'] = session['class_capacity']
            except:
                session_data['enrollment_capacity'] = "N/A"
            
            try:
                session_data['current_enrolled'] = session['enrollment_total']
            except:
                session_data['current_enrolled'] = "N/A"
            
            try:
                session_data['waitlist_capacity'] = session['wait_cap']
            except:
                session_data['waitlist_capacity'] = "N/A"

            try:
                session_data['current_waitlisted'] = session['wait_tot']
            except:
                session_data['current_waitlisted'] = "N/A"

            try:
                session_data['days'] = session['meetings'][0]['days']
            except:
                session_data['days'] = "N/A"

            try:
                session_data['start_time'] = parse_time(session['meetings'][0]['start_time'].strip())
                session_data['end_time'] = parse_time(session['meetings'][0]['end_time'].strip())
            except:
                session_data['start_time'] = "N/A"
                session_data['end_time'] = "N/A"

            detailed_info_array.append(session_data)

        detailed_info[(subject_mnemonic, catalog_nbr)] = detailed_info_array
    
    #print(detailed_info)
    

@app.route('/search', methods=['POST'])
def search():
    search_input = request.json['searchInput']
    academic_level_filter = request.json['academicLevelFilter']
    semester_filter = request.json['semesterFilter']
    json_results = get_top_search_results_json(search_input, academic_level_filter=academic_level_filter, semester_filter=semester_filter, n=10)
    return json_results


@app.route('/similar_courses', methods=['POST'])
def similar_courses():
    mnemonic, catalog_number = str(request.json['mnemonic']), str(request.json['catalog_number'])
    academic_level_filter = str(request.json['academicLevelFilter'])
    semester_filter = str(request.json['semesterFilter'])

    json_results = get_similar_courses(mnemonic, catalog_number, academic_level_filter=academic_level_filter, semester_filter=semester_filter, n=10)
    return json_results


@app.route('/detailed_info', methods=['POST'])
def get_detailed_info():
    '''
    print(detailed_info.keys())
    print("Getting detailed info")
    '''

    catalog_nbr = str(request.json['catalog_number'])
    subject_mnemonic = str(request.json['mnemonic'])

    #print((subject_mnemonic, catalog_nbr))

    if (subject_mnemonic, catalog_nbr) in detailed_info:
        #print("About to return detailed info initially")
        #print(detailed_info[(subject_mnemonic, catalog_nbr)])
        return detailed_info[(subject_mnemonic, catalog_nbr)]
    else:
        while (subject_mnemonic, catalog_nbr) not in detailed_info:
            time.sleep(0.5)
        #print("About to return detailed info after waiting")
        #print(detailed_info[(subject_mnemonic, catalog_nbr)])
        return detailed_info[(subject_mnemonic, catalog_nbr)]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)