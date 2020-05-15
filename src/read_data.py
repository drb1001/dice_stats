from flask import jsonify


def read_data_from_db(app, db, Model, parsed_input):
    """ """

    if parsed_input['const_sign'] == '+':
        const_mod = int(parsed_input['const'])
    elif parsed_input['const_sign'] == '-':
            const_mod = -1 * int(parsed_input['const'])
    else:
        const_mod = 0


    if parsed_input['kh_mod'] is None:

        rolls = (Model.query
                .filter_by(dice_total=parsed_input['num'])
                .filter_by(side_count=parsed_input['sides'])
                .all()
        )

        return [{'pip_total': r.pip_total + const_mod, 'probability': r.probability} for r in rolls]
