from flask import Flask, render_template, request,flash
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))

@app.route("/", methods=['GET'])
def index():

    return render_template("index.html")

standard_to = StandardScaler()

@app.route("/predict", methods=['POST','GET'])
def predict():
    if request.method == 'POST':
        # Present_Price = request.form.get('show_price')
        # Present_Price = float(Present_Price)
        Present_Price = int(10)
        Kms_Driven = int(request.form.get('Kilometers'))
        trans_type = request.form.get('trans_type')
        if trans_type == "Manual":
            Transmission_Manual = 1
        else:
            Transmission_Manual = 0

        Owner = int(request.form.get('owners'))
        fuel = request.form.get('fuel')
        if fuel == 'Petrol':
            Fuel_Type_Diesel = 0
            Fuel_Type_Petrol = 1
        elif fuel == 'Diesel':
            Fuel_Type_Diesel = 1
            Fuel_Type_Petrol = 0
        else:
            Fuel_Type_Diesel = 0
            Fuel_Type_Petrol = 0

        sealer_type = request.form.get('sealer')
        if (sealer_type == 'Dealer'):
            Seller_Type_Individual = 0
        else:
            Seller_Type_Individual = 1

        year = request.form.get('year')
        year = int(year)
        no_year = int(2021 - year)

        prediction = model.predict([[Present_Price, Kms_Driven, Owner, no_year, Fuel_Type_Diesel,
        Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Manual]])
        output=round(prediction[0],2)
        output = output
        if output<0:

            return render_template('index.html',output="Sorry you cannot sell this car")
        else:
            flash(output)
            return render_template('index.html',output = "You Can Sell The Car at",output2=" {} Lakhs".format(output))
    else:

        return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)
