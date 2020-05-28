
def read_data_from_db(app, db, Model, parsed_input):
    """ """

    if parsed_input['kh_mod'] is not None:
        rolls = (Model.query
                .filter_by(dice_total=parsed_input['num'])
                .filter_by(side_count=parsed_input['sides'])
                .filter_by(roll_type=parsed_input['kh_mod'])
                .all()
        )

    elif parsed_input['r_mod'] in ['r<', 'ro<']:
        rolls = (Model.query
                .filter_by(dice_total=parsed_input['num'])
                .filter_by(side_count=parsed_input['sides'])
                .filter_by(roll_type=parsed_input['r_mod'] + str(parsed_input['r_val']))
                .all()
        )

    else:
        rolls = (Model.query
                .filter_by(dice_total=parsed_input['num'])
                .filter_by(side_count=parsed_input['sides'])
                .filter_by(roll_type='base')
                .all()
        )

    return [{'pip_total': r.pip_total + parsed_input['const'], 'probability': r.probability} for r in rolls]
