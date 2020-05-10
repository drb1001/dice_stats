import os
from flask import Flask, request, render_template, jsonify
from waitress import serve

from utils import tidy_input, parse_input
from read_data import read_data_from_db
from populate_tables import create_tables, repopulate_roll_table


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning


from models import db, RollModel, RollDetailModel
db.init_app(app)
with app.app_context():
    create_tables(app, db)
    repopulate_roll_table(app, db)


@app.route('/', methods=['GET'])
def show_dice_stats():

    d1_input = request.args.get('d1', None, type=str)
    d2_input = request.args.get('d2', None, type=str)
    app.logger.info('D1 Input: {}; D2 input: {}'.format(d1_input, d2_input))

    # if d1_input is not None and d1_input != '':
    #     d1_input_tidy = tidy_input(d1_input)
    #     d1_input_parsed = parse_input(d1_input_tidy)
    # else:
    #     d1_input_parsed = ''
    #     d1_input = ''
    #
    # if d2_input is not None and d2_input != '':
    #     d2_input_tidy = tidy_input(d2_input)
    #     d2_input_parsed = parse_input(d2_input_tidy)
    #     d2_output = read_data_from_db(app, db, RollModel, d2_input_parsed)
    # else:
    #     d2_input_parsed = ''
    #     d2_output = ''
    #     d2_input = ''
    #
    # context_dict = {'text_1a': d1_input_parsed, 'text_1b': d1_output, 'd1_value': d1_input,
    #                 'text_2a': d2_input_parsed, 'text_2b': d2_output, 'd2_value': d2_input}

    context_dict = {'d1_value': d1_input, 'd2_value': d2_input}

    return render_template('template.html', **context_dict)


@app.route('/get_data', methods=['GET'])
def get_data():

    input = request.args.get('d', None, type=str)
    app.logger.info('get_data input:'.format(input))

    # TODO: find a better way of cleaning the input
    if input is not None and input != '':
        input_tidy = tidy_input(input)
        input_parsed = parse_input(input_tidy)
        output = read_data_from_db(app, db, RollModel, input_parsed)
    return jsonify(output)


# sanity check route
@app.route('/canary', methods=['GET'])
def canary():
    return jsonify('tweet tweet!')


if __name__ == '__main__':

    port = int(os.environ.get("FLASK_PORT", 5000))
    env = os.environ.get("APP_ENV")

    if env == "LOCAL_DEV":
        print("In dev now")
        app.run(host='0.0.0.0', port=port, debug=True)
    else:
        print("In prod now")
        serve(app, host="0.0.0.0", port=port)
