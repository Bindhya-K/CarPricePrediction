from flask import Flask,render_template,request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
import datetime  
import os 
app = Flask(__name__)
file_name = 'car_prediction.pkl'
try:
    with open(file_name,'rb') as file:
        unpickler = pickle.Unpickler(file)
        model = unpickler.load()
except EOFError:
    model=list()
#model = pickle.load(open('car_prediction.pkl','rb'))
@app.route('/', methods = ['GET'])
def Home():
    return render_template('index.html')
@app.route("/predict", methods=['POST'])
def predict():
    if request.method=='POST':
        Year = int(request.form['Year'])
        Present_Price = float(request.form['Present_Price'])
        Kms_Driven = int(request.form['Kms_Driven'])
        Owner = int(request.form['Owner'])
        Fuel_Type = request.form['Fuel_Type']
        if(Fuel_Type == 'Petrol'):
            Fuel_Type = 1
        elif(Fuel_Type =='Diesel'):
            Fuel_Type = 2
        else:
            Fuel_Type =3
        Year = datetime.date.today().year - Year
        Seller_Type = request.form['Seller_Type']
        if(Seller_Type=='Dealer'):
            Seller_Type = 0
        else:
            Seller_Type =1
        Transmission = request.form['Transmission']
        if (Transmission == 'Manual'):
            Transmission = 0
        else:
            Transmission =1
        prediction = model.predict([[Present_Price,Kms_Driven,Fuel_Type,Seller_Type,Transmission,Owner,Year]])
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {}".format(output))
    else:
         return render_template('index.html')
if __name__=="__main__":
    app.run(debug=True)
