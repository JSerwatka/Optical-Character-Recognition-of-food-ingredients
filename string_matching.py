# TODO
# 1. test app if leave one space during filtering in fuzzy_string_matching_ratio or leave no space

from fuzzywuzzy import fuzz
# from operator import itemgetter <- used only match_string_with_database option 1
import sqlite3 as sql
import re
# remider of how to import Levenshten C Python extansion module: https://github.com/ztane/python-Levenshtein
# from Levenshtein import *


# An iterator that uses fetchmany to keep memory usage down
# -> code from http://code.activestate.com/recipes/137270-use-generators-for-fetching-large-db-record-sets/
def result_iter(cursor, array_size: int = 1000):
    while True:
        results = cursor.fetchmany(array_size)
        if not results:
            break
        for result in results:
            yield result


def fuzzy_string_matching_ratio(string_from_OCR: str, string_from_db: str) -> int:
    # Force lowercase characters to make levenshtein more accurate
    string_from_OCR, string_from_db = string_from_OCR.lower(), string_from_db.lower()

    # Filter all characters that are not present in substances' names
    regex_to_filter_noise_from_string = re.compile('[^a-zA-Z0-9\'-/ ]')
    string_from_OCR = regex_to_filter_noise_from_string.sub("", string_from_OCR)
    string_from_db = regex_to_filter_noise_from_string.sub("", string_from_db)

    # Filter additional spaces
    string_from_OCR = ' '.join(filter(None, string_from_OCR.split(' ')))

    # Return Levenshtein ratio of input strings
    return fuzz.ratio(string_from_OCR, string_from_db)


def match_string_with_database(string_from_OCR: str) -> str:
    # local variable to store e_code with current max value of ratio
    max_ratio = 0

    conn = sql.connect('product_substances.db')
    cursor = conn.cursor()

    # Check if string is in 'e-code' format
    string_from_OCR_no_space = ''.join(filter(None, string_from_OCR.split(' ')))
    e_check_regex = re.compile("^.{0,2}[0-9]{2,3}.{0,2}$")
    if re.match(e_check_regex, string_from_OCR_no_space):
        # Take 2nd column
        cursor.execute("SELECT e_code FROM substances")
    else:
        # Take 1st column
        cursor.execute("SELECT name_of_substance FROM substances")

    # looking for max similarity between words
    for list_of_substances in result_iter(cursor, 100):
        if list_of_substances[0] is not None:
            ratio_for_current_e_code = fuzzy_string_matching_ratio(string_from_OCR, list_of_substances[0])
            if ratio_for_current_e_code > max_ratio:
                max_ratio = ratio_for_current_e_code
                substance_with_max_ratio = list_of_substances[0]
            # break the loop for 100% match
            if max_ratio == 100:
                break


print(match_string_with_database("kw2as v4gdhnaskorbinowy"))

'''
    # fetchall method + test of 2 solutions for database iterating and applying fuzzy_string_matching_ratio
    list_of_substances = cursor.fetchall()

    # option 1 - using build-in functions and itemgetter
    # <- 0.0005826806 s to execute with simpler function than fuzzy_string_matching_ratio
    # [x[0] for x in list_of_substances if x[0] is not None] <- takes all elements, extract from tuple and get rid of all None

    list_substance_and_ratio = map(lambda x: (x, fuzzy_string_matching_ratio(string_from_OCR, x)), [x[0] for x in list_of_substances if x[0] is not None])
    substance_with_max_ratio = max(list(list_substance_and_ratio), key=itemgetter(1))


    # option 2
    # <- 0.0005395729 s to execute with simpler function than fuzzy_string_matching_ratio
    for i in range(len(list_of_substances)):
        if list_of_substances[i][0] is not None:
            ratio_for_current_e_code = fuzzy_string_matching_ratio(string_from_OCR, list_of_substances[i][0])
            if ratio_for_current_e_code > code_with_max_ratio:
                code_with_max_ratio = ratio_for_current_e_code
                e_code_string = list_of_substances[i][0]
            # break the loop for 100% match
            if code_with_max_ratio == 100:
                break
'''
