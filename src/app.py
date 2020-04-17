import os
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from waitress import serve

from utils import tidy_input, parse_input
# from read_data import read_data_from_db


app = Flask(__name__)
# port = int(os.environ.get("PORT", 5000))
# app.config.from_object(os.environ['APP_SETTINGS'])

# app.config.from_object("config.DevelopmentConfig")
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# from models import RollModel, RollDetailModel


@app.route('/', methods=['GET'])
def index():
    """ """

    input = request.args.get('myInput', None, type=str)
    app.logger.info('Input: {}'.format(input))
    if input is not None:
        input_tidy = tidy_input(input)
        input_parsed = parse_input(input_tidy)
        # output = read_data_from_db(app, db, input_parsed)

        return render_template('template.html', text=input_parsed, value=input)

    return render_template('template.html', text='', value="")


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=5000)
    # app.run(host='0.0.0.0', port=5000, debug=True)
