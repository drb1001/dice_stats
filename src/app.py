import os
import json
import logging
from flask import Flask, request, render_template, jsonify
from waitress import serve

from utils import tidy_input, parse_input, calc_stats, InvalidInput
from read_data import read_data_from_db
from populate_tables import create_tables, repopulate_roll_table


SIDES_LIST = json.loads(os.getenv("SIDES_LIST", "[2,4,6,8,10,12,20]"))
MAX_DICE_TOTAL = int(os.getenv("MAX_DICE_TOTAL", "9"))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning


from models import db, RollModel
db.init_app(app)
with app.app_context():
    app.logger.debug('Building and populating database tables')
    create_tables(app, db)
    repopulate_roll_table(app, db, sides_list=SIDES_LIST, max_dice_total=MAX_DICE_TOTAL)
    app.logger.debug('Database tables populated')


@app.route('/', methods=['GET'])
def show_dice_stats():

    d1_input = request.args.get('d1', "", type=str)
    d2_input = request.args.get('d2', "", type=str)
    app.logger.info('D1 Input: {}; D2 input: {}'.format(d1_input, d2_input))
    context_dict = {'d1_value': d1_input, 'd2_value': d2_input, 'max_number_dice': MAX_DICE_TOTAL}
    return render_template('template.html', **context_dict)


@app.route('/get_data', methods=['GET'])
def get_data():
    input = request.args.get('d', None, type=str)
    app.logger.info('get_data input: {}'.format(input))

    if input is None or input == '':
        return jsonify("No input data"), 422
    else:
        try:
            input_tidy = tidy_input(input)
            app.logger.debug('input_tidy: {}'.format(input_tidy))

            input_parsed = parse_input(input_tidy, sides=SIDES_LIST, max_dice=MAX_DICE_TOTAL)
            app.logger.debug('input_parsed: {}'.format(input_parsed))

            rolls_output = read_data_from_db(app, db, RollModel, input_parsed)
            app.logger.debug('rolls_output: {}'.format(rolls_output))

            stats_output = calc_stats(roll_name=input_tidy, rolls=rolls_output)
            app.logger.debug('stats_output: {}'.format(stats_output))

            return jsonify({'rolls': rolls_output, 'stats': stats_output})

        except InvalidInput as e:
            app.logger.debug('Caught error: {}'.format(str(e)))
            return jsonify(str(e)), 422

        except e:
            app.logger.debug('Other unknown error')
            return jsonify(f"Unknown error {str(e)}"), 400


# sanity check route
@app.route('/canary', methods=['GET'])
def canary():
    return jsonify('tweet tweet!')


if __name__ == '__main__':

    port = int(os.environ.get("PORT", 5000))
    env = os.environ.get("APP_ENV")

    app.logger.info('Starting server')

    if env == "LOCAL_DEV":
        app.logger.setLevel(logging.DEBUG)
        app.logger.info('Running on dev server')
        app.run(host='0.0.0.0', port=port, debug=True)
    else:
        app.logger.info('Running on prod server')
        serve(app, host="0.0.0.0", port=port)
