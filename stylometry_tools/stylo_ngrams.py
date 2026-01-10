'''
A naive implementation of stylometry analysis.  Users can select how many n-grams
they want to use for the analysis. This module compares the 
frequency of individual letters in a control text to those in comparison samples.
'''

from typing import Dict, List
from utils import CharacterFrequencyDict, ERROR_DICT
import sys


ARGUMENTS = sys.argv


def main(ctrl_text: str, samples_list: List[str], number_of_ngrams: int = 1):
    run_stylometry_on_text(ctrl_text, samples_list, number_of_ngrams)
    exit(0)


def run_stylometry_on_text(
        ctrl_text: str,
        samples_text_list: List[str],
        number_of_ngrams: int = 1
    ):
    if ctrl_text is None:
        raise ERROR_DICT["CTRL_IS_NONE"]

    if samples_text_list is None:
        raise ERROR_DICT["SAMP_LIST_IS_NONE"]
    
    sample_scores = []
    ctrl_dict = create_character_hashtable(ctrl_text, number_of_ngrams)

    for index, sample in enumerate(samples_text_list):
        if sample is not None:
            sample_dict = create_character_hashtable(sample, number_of_ngrams)
            sample_score = tally_weighted_score(ctrl_dict, sample_dict)
            sample_scores.append(sample_score)
        else:
            print("Sample text at index " + str(index) + " is None, skipping sample.")
    
    print("Unigram stylometry complete")
    print(results_as_string(ctrl_dict, samples_text_list, sample_scores))


def run_stylometry_on_dict(ctrl_dict: CharacterFrequencyDict, samples_list: List[str]):
    if ctrl_dict is None:
        raise error_dict["CTRL_IS_NONE"]
    
    if samples_list is None:
        raise error_dict["SAMP_LIST_IS_NONE"]

    for sample in samples_list:
        if sample is not None:
            samp_dict = create_character_hashtable(sample)
            samp_score = str(tally_weighted_score(ctrl_dict, samp_dict))
            print("Unigram score between control and Sample: " + samp_score)
        else:
            print("Sample text is None, skipping sample.")
    
    print("Unigram stylometry complete")
    return results_as_string


def create_character_hashtable(text_samp: str, number_of_ngrams: int = 1) -> CharacterFrequencyDict:
    dict: CharacterFrequencyDict = {}
    lowercase_line = text_samp.lower()
    i = 0

    while i + number_of_ngrams - 1 < len(lowercase_line):
        ngram = ""
        # Create an n gram from n letters
        for n in range(number_of_ngrams):
            ngram += lowercase_line[i + n]
        if ngram not in dict and ngram is not None:
            dict[ngram] = 1
        elif ngram in dict:
            newvalue = dict[ngram]
            newvalue += 1
            dict[ngram] = newvalue
        i += 1

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
    main("Hello there", ["Bye there", "Bye Bye", "Yes"], int(sys.argv[1]))