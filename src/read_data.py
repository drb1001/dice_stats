from flask import jsonify

def read_data_from_db(app, db, Model, parsed_input):
    """ """

    if parsed_input['kh_mod'] is None:

        rolls = (Model.query
                .filter_by(dice_total=parsed_input['num'])
                .filter_by(side_count=parsed_input['sides'])
                .all()
        )

        app.logger.info('1 ------------------')

        app.logger.info(rolls)

        app.logger.info('2 ------------------')

        return [{'pip_total': r.pip_total, 'probability': r.probability} for r in rolls]



def read_data_from_db_api(app, db, RollModel, num, sides, kh_mod, kh_num):

    if parsed_input['kh_mod'] is None:

        rolls = (Model.query
                .filter_by(dice_total=num)
                .filter_by(side_count=sides)
                .all()
        )

        app.logger.info('1 ------------------')

        app.logger.info(rolls)

        app.logger.info('2 ------------------')

        return [{'pip_total': r.pip_total, 'probability': r.probability} for r in rolls]
