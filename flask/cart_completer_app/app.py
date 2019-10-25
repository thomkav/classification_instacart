# minimal example from:
# http://flask.pocoo.org/docs/quickstart/

import pickle
import numpy as np
import flask
import pandas as pd
from flask import render_template, request, Flask, jsonify
from flask_cors import CORS

import sys, os

import cart_api as api
assert api.convert_temp_from_unit

app = Flask(__name__)  # create instance of Flask class
CORS(app)



with open('./data/sample_user_orders.pkl', 'rb') as file:
    sample_user_orders = pickle.load(file)

@app.route('/')  # the site to route to
def api_test():

    # tables = [sample_user_orders.to_html(classes='ts1')]
    # titles = ['sample user orders']

    return render_template('user-viewer.html')    

@app.route('/get_user_order', methods=['GET','POST'])  # the site to route to
def get_user_orders():
    with open('data/sample_user_orders.pkl','rb') as file:
        sample_user_orders = pickle.load(file)
    
    user_id = int(request.args.get('user_id'))
    print(type(user_id))
    print(sample_user_orders)
    print("-----")
    print('user_id = ', user_id)
    print(sample_user_orders[sample_user_orders.user_id == user_id])
    return sample_user_orders[sample_user_orders.user_id == user_id].to_html()


@app.route('/view-user')  # the site to route to
def present_user_orders():

    tables = [sample_user_orders.to_html(classes='ts1')]
    titles = ['sample user orders']

    return render_template('user-viewer.html',tables=tables, titles=titles)        

@app.route('/convert_temperature', methods=['POST'])
def convert_temps():
    "Only route defined for this Flask app!"
    print(f"Input is {request.json}")

    try:
        result = api.convert_temp_from_unit(request.json['temperature'], request.json['unit'])
        status = 200
    except KeyError:
        result = {
            'message': 'Need to have input keys temperature and unit. Unit must be K, F, or C',
            'input': request.json
        }
        status = 400

    return jsonify(result), status



if __name__ == '__main__':
    app.run(debug=True)