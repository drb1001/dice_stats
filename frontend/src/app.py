import os
import json
import logging
from flask import Flask, request, render_template, jsonify
from waitress import serve


SIDES_LIST = json.loads(os.getenv("SIDES_LIST", "[2,3,4,6,8,10,12,20]"))
MAX_DICE_TOTAL = int(os.getenv("MAX_DICE_TOTAL", "20"))

app = Flask(__name__)

with app.app_context():
    app.logger.debug(f'SIDES_LIST: {SIDES_LIST}')
    app.logger.debug(f'SIDES_LIST: {MAX_DICE_TOTAL}')

@app.route('/', methods=['GET'])
def show_dice_stats():

    d1_input = request.args.get('d1', "", type=str)
    d2_input = request.args.get('d2', "", type=str)
    d3_input = request.args.get('d3', "", type=str)
    app.logger.info('D1 Input: {}; D2 input: {}; D3 input: {}'.format(d1_input, d2_input, d3_input))
    context_dict = {'d1_value': d1_input, 'd2_value': d2_input, 'd3_value': d3_input, 'max_number_dice': MAX_DICE_TOTAL}
    return render_template('template.html', **context_dict)


# sanity check route
@app.route('/canary', methods=['GET'])
def canary():
    return jsonify('tweet tweet!')


if __name__ == '__main__':

    port = int(os.environ.get("PORT", 5001))
    env = os.environ.get("APP_ENV")

    app.logger.info('Starting server')

    if env == "LOCAL_DEV":
        app.logger.setLevel(logging.DEBUG)
        app.logger.info('Running on dev server')
        app.run(host='0.0.0.0', port=port, debug=True)
    else:
        app.logger.info('Running on prod server')
        serve(app, host="0.0.0.0", port=port)
