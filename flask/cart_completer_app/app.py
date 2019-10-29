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

# with open('cart_completer_app/test.txt', 'w') as file:
#     file.write("test")

with open('cart_completer_app/data/merged_user_orders.pkl', 'rb') as file:
    merged_orders = pickle.load(file)

@app.route('/')  # the site to route to
def api_test():

    # tables = [sample_user_orders.to_html(classes='ts1')]
    # titles = ['sample user orders']

    return render_template('user-viewer.html')    


#########################
# RETURN ACTUAL USER CART
#########################
@app.route('/get_user_order_actual', methods=['GET','POST'])
def get_user_orders():
    # with open('data/actual_user_orders.pkl','rb') as file:
    #     sample_user_orders = pickle.load(file)
    
    user_id = int(request.args.get('user_id'))

    # Remove rows where add_to_cart_order is NaN.
    _ = merged_orders.dropna()

    table_output = (
        _[_.user_id == user_id][['product_name', 'add_to_cart_order','prev_order_ct']]
        ).sort_values('add_to_cart_order')

    html_output = table_output.style.set_table_styles(
            [
                {'selector': 'thead th',
            'props': [('background-color', 'AliceBlue')]},
                {'selector': 'thead th',
            'props': [('background-color', 'AliceBlue')]},
                ]).hide_index().render()

    status = 200

    return html_output, status

##############################
# FILTER / RETURN PREDICTION #
##############################
@app.route('/get_cart_prediction', methods=['GET','POST'])
def get_cart_prediction():
    try:
        # with open('data/model_preds.pkl','rb') as file:
        #     sample_user_orders = pickle.load(file)
        user_id = int(request.args.get('user_id'))
        
        _ = (merged_orders[merged_orders.user_id == user_id]
        ).sort_values('user_id').drop(
            labels=['product_id','user_id','order_id_ref','order_id','prev_order_ct'],
            axis=1
            )

        try:
            thresh = float(request.args.get('thresh'))
            print('got threshold values:',thresh)
        except:
            thresh = 0.5
        
        # Filter Threshold
        _ = _[_.pred_prob > thresh]
        _.sort_values(by=['pred_prob'], ascending=False, inplace=True)

        html_output = _.style.set_table_styles(
            [
                {'selector': 'thead th',
            'props': [('background-color', 'AliceBlue')]},
                {'selector': 'thead th',
            'props': [('background-color', 'AliceBlue')]},
                ]).hide_index().render()

        status = 200
        return html_output, status
    except:
        status = 400
        return None, status


# #########################
# # RETURN PREDICTION
# #########################
# @app.route('/get_cart_prediction', methods=['GET','POST'])
# def get_cart_prediction():
#     try:
#         with open('data/model_preds.pkl','rb') as file:
#             sample_user_orders = pickle.load(file)
#         user_id = int(request.args.get('user_id'))
        
#         df = (
#             sample_user_orders
#             [sample_user_orders.user_id == user_id]
#             ).sort_values('user_id')[['product_name', 'order_prob']]

#         html_output = df.style.set_table_styles(
#             [
#                 {'selector': 'thead th',
#             'props': [('background-color', 'AliceBlue')]},
#                 {'selector': 'thead th',
#             'props': [('background-color', 'AliceBlue')]},
#                 ]).hide_index().render()

#         status = 200
#         return html_output, status
#     except:
#         status = 400
#         return None, status













# @app.route('/view-user')  # the site to route to
# def present_user_orders():

#     tables = [sample_user_orders.to_html(classes='ts1')]
#     titles = ['sample user orders']

#     return render_template('user-viewer.html',tables=tables, titles=titles)        



# @app.route('/convert_temperature', methods=['POST'])
# def convert_temps():
#     "Only route defined for this Flask app!"
#     print(f"Input is {request.json}")

#     try:
#         result = api.convert_temp_from_unit(request.json['temperature'], request.json['unit'])
#         status = 200
#     except KeyError:
#         result = {
#             'message': 'Need to have input keys temperature and unit. Unit must be K, F, or C',
#             'input': request.json
#         }
#         status = 400

#     return jsonify(result), status



if __name__ == '__main__':
    app.run(debug=True)