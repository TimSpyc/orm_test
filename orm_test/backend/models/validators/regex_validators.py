import exrex
import re

def random_string_from_regex(pattern):
    return exrex.getone(pattern)

def does_string_match_regex(pattern, string):
    return re.match(pattern, string) is not None