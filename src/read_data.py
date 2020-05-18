from flask import jsonify


def read_data_from_db(app, db, Model, parsed_input):
    """ """

    rolls = (Model.query
            .filter_by(ndx_text=parsed_input['input_no_const'])
            .all()
    )

    return [{'pip_total': r.pip_total + parsed_input['const'], 'probability': r.probability} for r in rolls]
