import re

def tidy_input(input):
    """Takes the user input and parses / formats it
    """

    # remove spaces
    # if ends in kh, kl, dh, dl, append 1 on the end



    return imput


def check_parsed_input(parsed_input):
    """Check if the (parsed) input is in the tables

    Expeceted input is of the form ndxkhm+c
    """

    assert re.match("^[0-9]+d[0-9]+ [kh|kl|dh|dl]{0,1}[0-9]{0}  []$").match(parsed_input)

    n = int()
    x = int()
    kd_mod =
    m = int()
    c = int()

    assert n >= 0 and n<=20
    assert x in [2,3,4,5,6,8,10,12,20]
    assert m >=0 and m<=20
    assert m < n

    return {
        'input': parsed_input,
        'n': n,
        'x': x,
        'kd_mod': kd_mod,
        'm': m,
        'c': c
    }



# 10d6
# 2d12+5
# 1d100-1
# 2d20dl1
# 5d4kh3+3
