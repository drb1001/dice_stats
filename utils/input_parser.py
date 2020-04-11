import re


class InvalidInput(Exception):
    pass


def tidy_input(input):
    """Takes the user input and parses / formats it
    """
    assert isinstance(input, str)

    input_tidy = input.replace(" ", "")
    if input_tidy.endswith(('kh', 'kl', 'dh', 'dl')):
        input_tidy = input_tidy + '1'

    return input_tidy


def parse_input(input):
    """Check if the (parsed) input is in the tables

    Expeceted input is of the form ndxkhm+c
    """

    regex_str = r"""^(?P<num>[0-9]+)d(?P<sides>[0-9]+)((?P<kh_mod>kh|kl|dh|dl)(?P<kh_num>[0-9]+))?((?P<const_sign>\+|\-)(?P<const>[0-9]+))?$"""
    regex_match = re.match(regex_str, input)

    if not regex_match:
        raise InvalidInput(input, regex_match)

    parsed_input = regex_match.groupdict()
    for i in ['num', 'sides', 'kh_num', 'const']:
        parsed_input[i] = int(parsed_input[i]) if parsed_input[i] is not None else 0
    parsed_input['input'] = input

    if parsed_input['num'] not in range(1,20) : raise InvalidInput(parsed_input, 1)
    if parsed_input['sides'] not in [2,3,4,5,6,8,10,12,20] : raise InvalidInput(parsed_input, 2)
    if parsed_input['kh_num'] is not None:
        if parsed_input['kh_num'] not in range(0,20) : raise InvalidInput(parsed_input, 3)
        if parsed_input['kh_num'] >= parsed_input['num'] : raise InvalidInput(parsed_input, 4)

    return parsed_input
