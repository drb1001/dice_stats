import os
import logging
from flask import Flask, request, render_template, jsonify, abort
from waitress import serve

from utils import tidy_input, parse_input, calc_stats
from read_data import read_data_from_db
from populate_tables import create_tables, repopulate_roll_table


app = Flask(__name__)
app.logger.info('App created')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning
app.logger.info('DATABASE_URL config set')


from models import db, RollModel, RollDetailModel
db.init_app(app)
with app.app_context():
    create_tables(app, db)
    repopulate_roll_table(app, db)
app.logger.info('Database tables populated')


@app.route('/', methods=['GET'])
def show_dice_stats():

    d1_input = request.args.get('d1', "", type=str)
    d2_input = request.args.get('d2', "", type=str)
    app.logger.info('D1 Input: {}; D2 input: {}'.format(d1_input, d2_input))

    context_dict = {'d1_value': d1_input, 'd2_value': d2_input}
    return render_template('template.html', **context_dict)


@app.route('/get_data', methods=['GET'])
def get_data():
    input = request.args.get('d', None, type=str)
    app.logger.info('get_data input: {}'.format(input))

    # TODO: find a better way of cleaning the input
    if input is None or input == '':
        abort(400)
    else:
        input_tidy = tidy_input(input)
        app.logger.info('input_tidy: {}'.format(input_tidy))
        input_parsed = parse_input(input_tidy)
        app.logger.info('input_parsed: {}'.format(input_parsed))

        rolls_output = read_data_from_db(app, db, RollModel, input_parsed)
        stats_output = calc_stats(app, name=input_tidy, rolls=rolls_output)

        return jsonify({'rolls': rolls_output, 'stats': stats_output})


# sanity check route
@app.route('/canary', methods=['GET'])
def canary():
    return jsonify('tweet tweet!')


if __name__ == '__main__':

    port = int(os.environ.get("PORT", 5000))
    env = os.environ.get("APP_ENV")

    app.logger.info('Starting server')

    if env == "LOCAL_DEV":
        app.logger.setLevel(logging.INFO)
        app.logger.info('In dev now')
        app.run(host='0.0.0.0', port=port, debug=True)
    else:
        app.logger.info('In prod now')
        serve(app, host="0.0.0.0", port=port)
