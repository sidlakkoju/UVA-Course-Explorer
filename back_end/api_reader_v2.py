import requests
import threading
import pandas as pd

"""
multithreaded script to fetch data from the sis api for the past six semesters

loop over all the semesters
      - multithreaded???
      - for each semester, get the filtered csv with the in depth descriptions
      - keep saving to the csv
      - have print outputs for each page
      - store the past 6 semesters

- remove unnecessary columns
- add column for in-depth description
- add column for semster offerred

2023 spring
2022 fall
2022 spring
2022 fall
2021 spring
2021 fall
"""

output_file_lock = threading.Lock()

def get_base_url(year=2023, term="spring"):
    year_str = str(year)[-2:]
    term_num = 8
    if term == "spring":
        term_num = 2
    return f"https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1{year_str}{term_num}"


def get_single_page_results(year, term, page):
    url = get_base_url(year, term) + f"&page={page}"
    r = requests.get(url).json()
    return r


def get_all_courses_in_semester(year, term, output_file):
    courses = []
    page = 1
    while True:
        start_url = get_base_url(year, term) + f"&page={page}"
        r = requests.get(start_url).json()
        if len(r) == 0:
            break
        courses += r
        print(f"Got results for page {page} of {term} {year}")
        page += 1   # go to the next page


    df = pd.DataFrame(courses)

    # acquire lock before writing/appending to common file
    with output_file_lock:
        # check if the header has already been written
        try:
            with open(output_file, "r") as file:
                header = len(file.readline().strip()) == 0
        except FileNotFoundError:
            header = True
        df.to_csv(output_file, mode="a", header=header, index=False)


def main():
    # semesters = [
    #     (2021, "fall"),
    #     (2022, "spring"),
    #     (2022, "fall"),
    #     (2023, "spring")]
    semesters = [
        (2023, "fall")
    ]
    
    output_file = "prev_semester_data.csv"
    threads = []
    for (year, term) in semesters:
        thread = threading.Thread(target=get_all_courses_in_semester, args=(year, term, output_file))
        thread.start()
        threads.append(thread)
    
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()