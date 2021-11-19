
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


def read_data_from_db_json(app, db, Model, parsed_input):
    """ """

    if parsed_input['kh_mod'] is not None:
        roll_type=parsed_input['kh_mod']
    elif parsed_input['r_mod'] in ['r<', 'ro<']:
        roll_type=parsed_input['r_mod']+str(parsed_input['r_val'])
    else:
        roll_type='base'

    rolls = (
        Model.query
        .filter_by(dice_total=parsed_input['num'])
        .filter_by(side_count=parsed_input['sides'])
        .filter_by(roll_type=roll_type)
        .all()
    )

    rolls_prob = rolls[0].rolls_prob
    return [{'pip_total': int(r) + parsed_input['const'], 'probability': rolls_prob[r]}
                for r in rolls_prob.keys()]
