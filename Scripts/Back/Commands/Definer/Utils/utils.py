from difflib import SequenceMatcher

def is_strings_similar(first, second, threshold: float):
    if (type(first) == list):
        return is_string_to_list_similar(first, second, threshold)
    elif (type(second) == list):
        return is_string_to_list_similar(second, first, threshold)

    matcher = SequenceMatcher(None, first, second)

    return matcher.ratio() > threshold

def is_string_to_list_similar(list, string, threshold: float):
    for v in list:
        matcher = SequenceMatcher(None, v, string)
        if matcher.ratio() > threshold:
            return True

    return False

def is_similar_string_in_dictionary(dictionary, string, threshold: float = 0.8):
    for k, v in dictionary.items():
        if (is_strings_similar(v, string, threshold) or is_string_in_list(v, string)):
            return True, k

    return False

def is_string_in_list(list, string):
    for v in list:
        if (v in  string):
            return True

    return False