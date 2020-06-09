
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
                for r in rolls]

    elif parsed_input['r_mod'] in ['r<', 'ro<']:
        rolls = (Model.query
                .filter_by(dice_total=parsed_input['num'])
                .filter_by(side_count=parsed_input['sides'])
                .filter_by(roll_type='base')
                .order_by("id")
                .all()
        )
        return [{'pip_total': r.pip_total + parsed_input['const'],
                'probability': r.get_r_data(parsed_input['r_mod'], parsed_input['r_val'])}
                for r in rolls]

    else:
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
