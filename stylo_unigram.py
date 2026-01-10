'''
A naive implementation of unigram stylometry analysis.
Compares the frequency of individual letters in a control text to those in comparison samples.
'''

from typing import Dict, TypedDict, List


error_dict = {
    "CTRL_IS_NONE": ValueError("Control text cannot be None"),
    "SAMP_IS_NONE": ValueError("At least one comparison sample is required"),
    "SAMP_LIST_IS_NONE": ValueError("Comparison samples list cannot be None"),
}


class CharacterFrequencyDict(TypedDict):
    character: str
    frequency: int


def main(ctrl_text: str, samples_list: List[str]):
    run_unigram_stylometry_on_text(ctrl_text, samples_list)
    exit(0)


def run_unigram_stylometry_on_text(ctrl_text: str, samples_text_list: List[str]):
    if ctrl_text is None:
        raise error_dict["CTRL_IS_NONE"]

    if samples_text_list is None:
        raise error_dict["SAMP_LIST_IS_NONE"]
    
    sample_scores = []
    ctrl_dict = create_character_hashtable(ctrl_text)

    for index, sample in enumerate(samples_text_list):
        if sample is not None:
            sample_dict = create_character_hashtable(sample)
            sample_score = tally_weighted_score(ctrl_dict, sample_dict)
            sample_scores.append(sample_score)
        else:
            print("Sample text at index " + str(index) + " is None, skipping sample.")
    
    print("Unigram stylometry complete")
    print(results_as_string(ctrl_dict, samples_text_list, sample_scores))


def results_as_string(ctrl_dict: dict, sample_list: List[str], sample_scores: List[str]):
    result_string = "\n~ Ctrl dictionary: " + str(ctrl_dict) + " ~\n\n~ "
    for sample in sample_list:
        result_string += str(sample) + " ~ "
    result_string += "\n~ "
    for score in sample_scores:
        result_string += str(score) + " ~ "
    return result_string


def run_stylometry_on_dict(ctrl_dict: dict, samples_list: List[str]):
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


def create_character_hashtable(text_samp: str) -> dict:
    dict = {}
    lowercase_line = text_samp.lower()
    for letter in lowercase_line:
        if letter.isalpha():
            if letter not in dict:
                dict.update([(letter, 1)])
            elif letter in dict:
                newvalue = dict.pop(letter)
                newvalue += 1
                dict.update([(letter, newvalue)])
    return dict


def tally_weighted_score(ctrl_dict: CharacterFrequencyDict, sample_dict: CharacterFrequencyDict) -> int:
    score = 0
    ctrl_keys = ctrl_dict.keys()
    for key in ctrl_keys:
        if key in sample_dict:
            freq_ctrl = ctrl_dict.get(key)
            freq_comp = sample_dict.get(key)
            if freq_comp >= 0.80 * freq_ctrl and freq_comp <= 1.20 * freq_ctrl:
                if freq_comp > 0.95 * freq_ctrl and freq_comp < 1.05 * freq_ctrl:
                    score += 2
                else:
                    score += 1
    return score


if __name__ == "__main__":
    main("Hello there", ["Bye there", "Bye Bye", "Yes"])