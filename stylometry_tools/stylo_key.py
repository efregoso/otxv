'''
A naive implementation of stylometry analysis.  Users can select how many n-grams
they want to use for the analysis. This module compares the 
frequency of individual letters in a control text to those in comparison samples.
'''

from typing import List
from utils import CharacterFrequencyDict, ERROR_DICT


def main(ctrl_text: str, samples_list: List[str]):
    run_keyword_stylometry_on_text(ctrl_text, samples_list)
    exit(0)


def run_keyword_stylometry_on_text(
        ctrl_text: str,
        samples_text_list: List[str]
    ):
    if ctrl_text is None:
        raise ERROR_DICT["CTRL_IS_NONE"]

    if samples_text_list is None:
        raise ERROR_DICT["SAMP_LIST_IS_NONE"]
    
    sample_scores = []
    ctrl_dict = create_keyword_hashtable(ctrl_text)

    for index, sample in enumerate(samples_text_list):
        if sample is not None:
            sample_dict = create_keyword_hashtable(sample)
            sample_score = tally_weighted_score(ctrl_dict, sample_dict)
            sample_scores.append(sample_score)
        else:
            print("Sample text at index " + str(index) + " is None, skipping sample.")
    
    print("Keyword stylometry complete")
    print(results_as_string(ctrl_dict, samples_text_list, sample_scores))


def create_keyword_hashtable(text_samp: str, number_of_ngrams: int = 1) -> CharacterFrequencyDict:
    dict: CharacterFrequencyDict = {}
    lowercase_line = text_samp.lower()
    split_line = lowercase_line.split(" ")

    for word in split_line:
        newword = ""
        for char in word:
            if char.isalpha():
                newword += char
        # if the dictionary does not have this word in it, add it
        if newword not in dict and len(newword) >= 4:
            dict[newword] = 1
        elif newword in dict:
            newvalue = dict[newword]
            newvalue += 1
            dict[newword] = newvalue
    return dict


def tally_weighted_score(ctrl_dict: CharacterFrequencyDict, sample_dict: CharacterFrequencyDict) -> int:
    score = 0
    ctrl_keys = ctrl_dict.keys()
    for key in ctrl_keys:
        if key in sample_dict:
            freq_ctrl: int = ctrl_dict[key]
            freq_comp: int = sample_dict[key]
            if freq_comp >= 0.80 * freq_ctrl and freq_comp <= 1.20 * freq_ctrl:
                if freq_comp > 0.95 * freq_ctrl and freq_comp < 1.05 * freq_ctrl:
                    score += 2
                else:
                    score += 1
    return score


def results_as_string(ctrl_dict: CharacterFrequencyDict, sample_list: List[str], sample_scores: List[str]):
    result_string = "\n~ Ctrl dictionary: " + str(ctrl_dict) + " ~\n\n~ "
    for sample in sample_list:
        result_string += str(sample) + " ~ "
    result_string += "\n~ "
    for score in sample_scores:
        result_string += str(score) + " ~ "
    return result_string


if __name__ == "__main__":
    main("Hello there", ["Hello there e", "Bye there", "Bye Bye", "Yes"])