import re


class InvalidInput(ValueError):
    pass


def tidy_input(input):
    """Takes the user input removes spaces and standardises other terms
    """

    assert isinstance(input, str)

    input_tidy = input.lower().replace(" ", "")

    return input_tidy


def parse_input(input, sides, max_dice):
    """Check if the (parsed) input is in the tables

    Outputs a dict with keys:
      - input: original input (str)
      - input_no_const: original input with const modifiers removed
      - num: number of dice (int)
      - sides: sides of each die (int)
      - kh_mod: the type of kh/dl modifier (str) - optional
      - r_mod: the type of reroll modifier (str) - optional
      - r_val: the value of the reroll modifier (int) - default 0
      - const_sign: sign of the constant value added (str) - optional
      - const: constant value added (int) - default 0
    """

    regex_str = r"""^(?P<num>[0-9]+)d(?P<sides>[0-9]+)((?P<kh_mod>kh|kl|dh|dl)|((?P<r_mod>r\<|ro\<)(?P<r_val>[0-9]+)))?((?P<const_sign>\+|\-)(?P<const>[0-9]+))?$"""
    regex_match = re.match(regex_str, input)

    if not regex_match:
        raise InvalidInput(f"The input ({input}) could not be parsed as a dice roll. See https://wiki.roll20.net/Dice_Reference")

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
    if parsed_input['num'] not in range(1, max_dice+1):
        raise InvalidInput(f"Invalid dice roll '{input}' - Number of dice ({parsed_input['num']}) must be between 1 and {max_dice}")
    if parsed_input['sides'] not in sides:
         raise InvalidInput(f"Invalid dice roll '{input}' - Number of sides ({parsed_input['sides']}) must be one of {sides}")
    if parsed_input['r_mod'] is not None and parsed_input['r_val'] not in [1,2]:
         raise InvalidInput(f"Invalid dice roll '{input}' - Currently only supported for: r<1, r<2, ro<1, ro<2")
    if parsed_input['r_mod'] is not None and parsed_input['r_val'] not in range(1, parsed_input['sides']):
        raise InvalidInput(f"Invalid dice roll '{input}' - the rerolls ({parsed_input['r_val']}) must be lower than the number of sides ({parsed_input['sides']})")
    if parsed_input['kh_mod'] is not None and (parsed_input['num'] != 2 and parsed_input['input_no_const'] != '4d6dl'):
        raise InvalidInput(f"Invalid dice roll '{input}' - kh/kl/dh/dl logic currently only supported for 2 dice (eg:2d20kh), or 4d6dl")

    return parsed_input
