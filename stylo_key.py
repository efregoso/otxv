

def main(ctrl_text, comp_samp1, comp_samp2, comp_samp3):
    ctrl = create_hashtable_alpha(ctrl_text)
    print(ctrl)
    samp1 = create_hashtable_alpha(comp_samp1)
    print(samp1)
    samp2 = create_hashtable_alpha(comp_samp2)
    print(samp2)
    samp3 = create_hashtable_alpha(comp_samp3)
    print(samp3)
    e = ctrl.keys()
    print("Keyword score between control and Sample 1: " + str(tally_weighted_score(ctrl, samp1, e)))
    print("Keyword score between control and Sample 2: " + str(tally_weighted_score(ctrl, samp2, e)))
    print("Keyword score between control and Sample 3: " + str(tally_weighted_score(ctrl, samp3, e)))
    print("Keyword stylometry done")
    exit(0)


def run_stylometry_on(list):
    ctrl_text = list[0]
    comp_samp1 = list[1]
    comp_samp2 = list[2]
    comp_samp3 = list[3]
    if ctrl_text is not None:
        ctrl = create_hashtable_alpha(ctrl_text)
        print(ctrl)
        e = ctrl.keys()
    if comp_samp1 is not None:
        samp1 = create_hashtable_alpha(comp_samp1)
        print(samp1)
        samp1score = str(tally_weighted_score(ctrl, samp1, e))
        print("Keyword score between control and Sample 1: " + samp1score)
    if comp_samp2 is not None:
        samp2 = create_hashtable_alpha(comp_samp2)
        print(samp2)
        samp2score = str(tally_weighted_score(ctrl, samp2, e))
        print("Keyword score between control and Sample 2: " + samp2score)
    if comp_samp3 is not None:
        samp3 = create_hashtable_alpha(comp_samp3)
        print(samp3)
        samp3score = str(tally_weighted_score(ctrl, samp3, e))
        print("Keyword score between control and Sample 3: " + samp3score)
    # turn into a string
    print("Keyword stylometry complete")
    result = str(ctrl) + "~" + str(samp1) + "~" + str(samp2) + "~" + str(samp3) + "~" + samp1score + "~" + samp2score + "~" + samp3score
    return result

def run_stylometry_on_dict(list):
    ctrl_text = list[0]
    comp_samp1 = list[1]
    comp_samp2 = list[2]
    comp_samp3 = list[3]
    if ctrl_text is not None:
        ctrl = create_hashtable_alpha(ctrl_text)
        print(ctrl)
        e = ctrl.keys()
    if comp_samp1 is not None:
        samp1 = create_hashtable_alpha(comp_samp1)
        print(samp1)
        samp1score = str(tally_weighted_score(ctrl, samp1, e))
        print("Keyword score between control and Sample 1: " + samp1score)
    if comp_samp2 is not None:
        samp2 = create_hashtable_alpha(comp_samp2)
        print(samp2)
        samp2score = str(tally_weighted_score(ctrl, samp2, e))
        print("Keyword score between control and Sample 2: " + samp2score)
    if comp_samp3 is not None:
        samp3 = create_hashtable_alpha(comp_samp3)
        print(samp3)
        samp3score = str(tally_weighted_score(ctrl, samp3, e))
        print("Keyword score between control and Sample 3: " + samp3score)
    # turn into a list
    print("Keyword stylometry complete")
    resultdict = {"ctrl_hash": ctrl, "samp1_hash": samp1, "samp2_hash": samp2, "samp3_hash": samp3, "samp1_score": samp1score, "samp2_score": samp2score, "samp3_score": samp3score}
    return resultdict

def create_hashtable_alpha(textsamp):
    dict = {}
    line = textsamp.lower()
    splitline = line.split(" ")
    print(str(splitline))
    # remove everything that isn't an alphanumeric character
    for word in splitline:
        newword = ""
        i = 0
        while i < len(word):
            if word[i].isalpha():
                newword += word[i]
            i = i + 1
        # if the dictionary does not have this word in it, add it
        if newword not in dict and len(newword) >= 4:
            dict.update([(newword, 1)])
        elif newword in dict:
            newvalue = dict.pop(newword)
            newvalue = newvalue + 1
            dict.update([(newword, newvalue)])
    return dict


def tally_weighted_score(control, compare, e):
    score = 0
    for key in e:
        if key in compare:
            freqctrl = control.get(key)
            freqcomp = compare.get(key)
            if freqcomp >= 0.75*freqctrl and freqcomp <=1.25*freqctrl:
                if freqcomp > 0.9*freqctrl and freqcomp < 1.1*freqctrl:
                    score = score + 2
                else:
                    score = score + 1
    return score


if __name__ == "__main__":
    main("Hellllllo butt", "Byeeeeee butt", "Byeeeeee Byeeeeee", "Holle")