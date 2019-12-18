from fuzzywuzzy import fuzz
import re
#remider of how to import Levenshten C Python extansion module: https://github.com/ztane/python-Levenshtein
#from Levenshtein import *


def fuzzy_string_matching(string_from_OCR: str, string_from_db: str) -> int:
    # Force lowercase characters to make levenshtein more accurate
    string_from_OCR, string_from_db = string_from_OCR.lower(), string_from_db.lower()

    # Filter all characters that are not present in substances' names
    regex_to_filter_noise_from_string = re.compile('[^a-zA-Z0-9\'-/ ]')
    string_from_OCR = regex_to_filter_noise_from_string.sub("", string_from_OCR)
    string_from_db = regex_to_filter_noise_from_string.sub("", string_from_OCR)

    # Filter additional spaces
    string_from_OCR = ' '.join(filter(None, string_from_OCR.split(' ')))

    # Return Levenshtein ratio of input strings
    return fuzz.ratio(string_from_OCR, string_from_db)