# from models import RollModel, RollDetailModel

def read_data_from_db(app, db, parsed_input):
    """ """

    if parsed_input['kh_mod'] is None:

        rolls = (Roll.query
                .filter(Roll.dice_total == parsed_input['num'])
                .filter(Roll.side_count == parsed_input['sides'])
        )

        return  jsonify([r.serialize() for r in rolls])
