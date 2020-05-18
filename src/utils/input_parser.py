import re


class InvalidInput(Exception):
    pass


def tidy_input(input):
    """Takes the user input removes spaces and standardises other terms
    """
    assert isinstance(input, str)

    input_tidy = input.lower().replace(" ", "")

    return input_tidy


def parse_input(input):
    """Check if the (parsed) input is in the tables

    Outputs a dict with keys:
      - input: original input (str)
      - input_no_const: original input with const modifiers removed
      - num: number of dice (int)
      - sides: sides of each die (int)
      - kh_mod: the type of kh/dl modifier (str) - optional
      - r_mod: the type of reroll modifier (str) - optional
      - r_val: the value od the reroll modifier (int) - default 0
      - const_sign: sign of the constant value added (str) - optional
      - const: constant value added (int) - default 0
    """

    regex_str = r"""^(?P<num>[0-9]+)d(?P<sides>[0-9]+)((?P<kh_mod>kh|kl|dh|dl)|((?P<r_mod>r\<|ro\<)(?P<r_val>[0-9]+)))?((?P<const_sign>\+|\-)(?P<const>[0-9]+))?$"""
    regex_match = re.match(regex_str, input)

    if not regex_match:
        raise InvalidInput(input, regex_match)

    parsed_input = regex_match.groupdict()

    parsed_input['input'] = input

    if parsed_input['const_sign'] is not None:
        parsed_input['input_no_const'] = input.replace(parsed_input['const_sign'] + parsed_input['const'], '')
    else:
        parsed_input['input_no_const'] = input

    for i in ['num', 'sides', 'r_val', 'const']:
        parsed_input[i] = int(parsed_input[i]) if parsed_input[i] is not None else 0
    if parsed_input['const_sign'] == '-':
        parsed_input['const'] = -1 * parsed_input['const']

    # do some validations:
    if parsed_input['num'] not in range(1,20) : raise InvalidInput(parsed_input, 1)
    if parsed_input['sides'] not in [2,3,4,5,6,8,10,12,20] : raise InvalidInput(parsed_input, 2)
    if parsed_input['r_mod'] is not None:
        if parsed_input['r_val'] not in range(1, parsed_input['sides']): raise InvalidInput(parsed_input, 3)

    return parsed_input
