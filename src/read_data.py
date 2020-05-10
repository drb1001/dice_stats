from flask import jsonify


def read_data_from_db(app, db, Model, parsed_input):
    """ """

    if parsed_input['kh_mod'] is None:

        rolls = (Model.query
                .filter_by(dice_total=parsed_input['num'])
                .filter_by(side_count=parsed_input['sides'])
                .all()
        )

        return [{'pip_total': r.pip_total, 'probability': r.probability} for r in rolls]
