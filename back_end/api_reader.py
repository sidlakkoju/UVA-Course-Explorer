import json
import pandas as pd
import requests


# class for query builder?
def get_base_url(year=2023, term="spring"):
    year_str = str(year)[-2:]
    term_num = 8
    if term == "spring":
        term_num = 2
    
    return f"https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1{year_str}{term_num}"
    # return f"https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=1{year_str}{term_num}"


# get subjects for a specific year and term
def write_subjects_to_csv(year=23, term="spring", output_filename="subjects.csv"):
    r = requests.get(get_base_url(year, term))
    response_dict = r.json()
    subjects = response_dict["subjects"]
    df = pd.DataFrame(subjects)
    df.to_csv(output_filename, index=False)


# https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1228&subject=CS&page=1

# https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=1232&subject=CS&page=1

# https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1228


# catalog number
# department
# course title
# course description
# undergraduate or graduate
# credits


def get_all_courses(year=23, term="spring", output_file="courses.csv"):
    courses = []
    page = 1
    start_url = get_base_url(year, term) + f"&page={page}"
    print(start_url)
    r = requests.get(start_url).json()
    while len(r) > 0:
        courses += r
        page += 1   # go to the next page
        print(f"requesting page {page}")
        start_url = get_base_url(year, term) + f"&page={page}"
        r = requests.get(start_url).json()
        print(r)

    df = pd.DataFrame(courses)
    df.to_csv(output_file, index=False)


    






    # # Convert dictionary to list of key-value pairs
    # dict_items = r.items()
    # list_of_tuples = list(dict_items)

    # # Create Pandas dataframe from list
    # df = pd.DataFrame(list_of_tuples, columns=['Key', 'Value'])
    # print(df)
    # Print dataframe
    # df.to_csv("test.csv")

    # print(r.keys())
    # print(type(r))






    



    # r = requests.get(get_base_url(year, term))


    # response_dict = r.json()
    # subjects = response_dict["subjects"]



get_all_courses()




"""
index                                                                     3
crse_id                                                                  84
crse_offer_nbr                                                            1
strm                                                                   1232
session_code                                                              1
session_descr                                      Regular Academic Session
class_section                                                           102
location                                                               MAIN
location_descr                                                   On Grounds
start_dt                                                         01/18/2023
end_dt                                                           05/02/2023
class_stat                                                                A
campus                                                                 MAIN
campus_descr                                                    Main Campus
class_nbr                                                             10005
acad_career                                                            UGRD
acad_career_descr                                             Undergraduate
component                                                               DIS
subject                                                                 AAS
subject_descr                                    African-American & African
catalog_nbr                                                            1020
class_type                                                                N
schedule_print                                                            Y
acad_group                                                             CGAS
instruction_mode                                                          P
instruction_mode_descr                                            In Person
acad_org                                                                AAS
wait_tot                                                                  0
wait_cap                                                                199
class_capacity                                                           20
enrollment_total                                                         20
enrollment_available                                                      0
descr                     Introduction to African-American and African S...
rqmnt_designtn                                                           NW
units                                                                     0
combined_section                                                          N
enrl_stat                                                                 C
enrl_stat_descr                                                      Closed
topic                                                                   NaN
instructors               [{'name': 'Dana Moyer', 'email': 'dkm4ra@virgi...
section_type                                                     Discussion
meetings                  [{'days': 'Tu', 'start_time': '17.00.00.000000...
crse_attr                                                              ASUD
crse_attr_value                                           ASUD-CSW,ASUD-SES
reserve_caps                                                             []
combined_descr                                                          NaN
reserved_combined_info                                                  NaN
Name: 2, dtype: object
"""