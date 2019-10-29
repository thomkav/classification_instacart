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

with open('cart_completer_app/data/combined_model_preds.pkl', 'rb') as file:
    combined_model_preds = pickle.load(file)



unique_users = merged_orders.user_id.unique()
user_ct = len(unique_users)

@app.route('/')  # the site to route to
def api_test():

    # tables = [sample_user_orders.to_html(classes='ts1')]
    # titles = ['sample user orders']

    return render_template('user-viewer.html', user_ct=user_ct)    


#########################
# SWAP MODEL
#########################
@app.route('/select-model', methods=['GET','POST'])
def select_model():

    # tables = [sample_user_orders.to_html(classes='ts1')]
    # titles = ['sample user orders']

    return render_template('user-viewer.html', user_ct=user_ct)  



#########################
# RETURN ACTUAL USER CART
#########################
@app.route('/get_user_order_actual', methods=['GET','POST'])
def get_user_orders():
    
    user_ind = int(request.args.get('user_ind'))
    user_id = unique_users[user_ind]
    print(user_id)

    # Remove rows where add_to_cart_order is NaN.
    _ = merged_orders.dropna()

    _ = (_[_.user_id == user_id][['product_name', 'add_to_cart_order','prev_order_ct']]
        ).sort_values('add_to_cart_order')[['add_to_cart_order', 'product_name']]
    
    _.columns = ['Add Order', 'Product']

    # def highlight_user_cart_matches(s):
    #     if s['add_to_cart_order'] > 0:
    #         return ['background-color: lightgreen'] * col_length
    #     else:
    #         return ['background-color: lightgray'] * col_length

    html_output = _.style.hide_index().render()

    # html_output = table_output.style.set_table_styles(
    #         [
    #             {'selector': 'thead th',
    #         'props': [('background-color', 'AliceBlue')]},
    #             {'selector': 'thead th',
    #         'props': [('background-color', 'AliceBlue')]},
    #             ]).hide_index().render()

    status = 200

    return jsonify({"html_output": html_output, 'user_id': str(user_id)})

##############################
# FILTER / RETURN PREDICTION #
##############################
@app.route('/get_cart_prediction', methods=['GET','POST'])
def get_cart_prediction():
    try:
        # with open('data/model_preds.pkl','rb') as file:
        #     sample_user_orders = pickle.load(file)
        user_ind = int(request.args.get('user_ind'))
        user_id = unique_users[user_ind]
        
        _ = (merged_orders[merged_orders.user_id == user_id]
        ).sort_values('user_id').drop(
            labels=['product_id','user_id','order_id_ref','order_id','prev_order_ct'],
            axis=1
            )

        try:
            rec_count = int(request.args.get('rec_count'))
            print('got threshold values:',rec_count)
        except:
            rec_count = 0.5
        
        # Filter Threshold
        # _ = _[_.pred_prob > thresh]
        
        # Recommendation Count Threshold
        _.sort_values(by=['pred_prob'], ascending=False, inplace=True)
        _ = _[['add_to_cart_order', 'product_name']]
        _.columns = ['Add To Cart Order', 'Product']
        _ = _[:rec_count]

        cart_metrics = f'Relevancy: {round(_.dropna().shape[0]/_.shape[0], 3)*100}%'

        # print(_)

        col_length = len(_.columns)

        def highlight_user_cart_matches(s):
            if s['Add To Cart Order'] > 0:
                return ['background-color: lightgreen'] * col_length
            else:
                return ['background-color: lightgray'] * col_length

        html_output = _.style.apply(highlight_user_cart_matches, axis=1).hide_columns(subset=['Add To Cart Order']).hide_index().render()

        # html_output = _.style.set_table_styles(
        #     [
        #         {'selector': 'thead th',
        #     'props': [('background-color', 'AliceBlue')]},
        #         {'selector': 'thead th',
        #     'props': [('background-color', 'AliceBlue')]},
        #         ]).hide_index().render()

        status = 200
        return jsonify({'html_output': html_output, 'status': status, 'cart_metrics':cart_metrics})
    except:
        status = 400
        return None, status

if __name__ == '__main__':
    app.run(debug=True)