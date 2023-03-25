import json
import pandas as pd
import requests


# class for query builder?
def get_base_url(year=2023, term="spring"):
    year_str = str(year)[-2:]
    term_num = 8
    if term == "spring":
        term_num = 2
    return f"https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=1{year_str}{term_num}"


# get subjects for a specific year and term
def write_subjects_to_csv(year=23, term="spring", output_filename="subjects.csv"):
    r = requests.get(get_base_url(year, term))
    response_dict = r.json()
    subjects = response_dict["subjects"]
    df = pd.DataFrame(subjects)
    df.to_csv(output_filename, index=False)


def get_all_courses_for_a_subject(subject, year=23, term="spring"):
    page = 0
    start_url = get_base_url(year, term) + f"&subject={subject}" + f"&page={page}"


    r = requests.get(get_base_url(year, term))

    
    # response_dict = r.json()
    # subjects = response_dict["subjects"]
    # df = pd.DataFrame(subjects)
    # df.to_csv(output_filename, index=False)




write_subjects_to_csv()
