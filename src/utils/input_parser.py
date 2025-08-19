import re
from decimal import Decimal


class InvalidInput(ValueError):
    pass

class InvalidProbability(ValueError):
    pass


def tidy_input(input):
    """Takes the user input removes spaces and standardises other terms
    """

    assert isinstance(input, str)

    input_tidy = input.lower().replace(" ", "")

    return input_tidy


def split_input(input):
    """Takes the user input and splits into calcuatable parts
    """

    assert isinstance(input, str)

    input_split = input.replace("-","+-").split("+")

    return input_split


def is_simple_int(input):
    """ """
    try:
        int(input)
    except ValueError:
        return False
    else:
        return True


def get_data_parts(input_part, sides, max_dice, app, db, model):
    """ """

    if is_simple_int(input_part):
        int_value = int(input_part)
        rolls_output = [{'pip_total': int_value, 'probability': Decimal('1.0')}]
        app.logger.debug('rolls_output: {}'.format(rolls_output))
    else:
        input_parsed = parse_input(input_part, sides=sides, max_dice=max_dice)
        app.logger.debug('input_parsed: {}'.format(input_parsed))

        rolls_output = read_data_from_db(app, db, model, input_parsed)
        app.logger.debug('rolls_output: {}'.format(rolls_output))

    return rolls_output


def check_probability_total(rolls, tolerance=0.01):
    """ """

    total_prob = 0
    for r in rolls:
         total_prob += r['probability']
    if abs(1.0 - float(total_prob)) > tolerance:
        raise InvalidProbability(f"Something went wrong calculating the probability distribution ({round(total_prob, 5)})")


def calculate_rolls(input_split, sides, max_dice, app, db, model):
    """ """

    outputs = []

    for input_part in input_split:
        rolls_output = get_data_parts(input_part, sides, max_dice, app, db, model)
        outputs.append(rolls_output)
        app.logger.debug('outputs: {}'.format(outputs))

    # combine
    for ix, input_part in enumerate(outputs):
        if ix == 0:
            running_rolls = input_part
        else:
            temp = [{
                    'pip_total': r['pip_total'] + i['pip_total'],
                    'probability': r['probability'] * i['probability']
                    } for r in running_rolls for i in input_part]
            running_rolls = temp

    # sort to make things easier
    running_rolls = sorted(running_rolls, key = lambda x: x['pip_total'])
    app.logger.debug('running_rolls: {}'.format(running_rolls))


    # remove and combine duplicates
    simplified = []
    for r in running_rolls:
        is_done = False
        for s in simplified:
            if s['pip_total'] == r['pip_total']:
                s['probability'] = s['probability'] + r['probability']
                is_done = True
        if not is_done:
            simplified.append(r)

    check_probability_total(simplified)

    app.logger.debug('simplified: {}'.format(simplified))

    return simplified


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



def read_data_from_db(app, db, Model, parsed_input):
    """ """

    if parsed_input['kh_mod'] is not None:
        rolls = (Model.query
                .filter_by(dice_total=parsed_input['num'])
                .filter_by(side_count=parsed_input['sides'])
                .filter_by(roll_type=parsed_input['kh_mod'])
                .order_by("id")
                .all()
        )
        return [{'pip_total': r.pip_total + parsed_input['const'],
                'probability': r.base_prob}
                for r in rolls ]

    elif parsed_input['r_mod'] in ['r<', 'ro<']:
        min_roll = parsed_input['num'] * (parsed_input['r_val'] + 1) if parsed_input['r_mod'] == 'r<' else parsed_input['num']
        rolls = (Model.query
                .filter_by(dice_total=parsed_input['num'])
                .filter_by(side_count=parsed_input['sides'])
                .filter_by(roll_type='base')
                .order_by("id")
                .all()
        )
        return [{'pip_total': r.pip_total + parsed_input['const'],
                'probability': r.get_r_data(parsed_input['r_mod'], parsed_input['r_val'])}
                for r in rolls if r.pip_total >= min_roll]

    else:
        # regular old roll
        rolls = (Model.query
                .filter_by(dice_total=parsed_input['num'])
                .filter_by(side_count=parsed_input['sides'])
                .filter_by(roll_type='base')
                .order_by("id")
                .all()
        )
    return [{'pip_total': r.pip_total + parsed_input['const'],
            'probability': r.base_prob}
            for r in rolls]
