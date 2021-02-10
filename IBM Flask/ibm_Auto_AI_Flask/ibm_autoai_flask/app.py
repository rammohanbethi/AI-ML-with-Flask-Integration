import numpy as np
from flask import Flask, request, jsonify, render_template
import requests

import json
# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "MEnqAPHAxzwja60KLJ_kRCST7sye1ct23OUf2tiyB6q4"
token_response = requests.post('https://iam.eu-gb.bluemix.net/identity/token', data={"apikey": API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]
print("mltoken",mltoken)

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
#payload_scoring = {"input_data": [{"fields": [array_of_input_fields], "values": [array_of_values_to_be_scored, another_array_of_values_to_be_scored]}]}


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/y_predict',methods=['POST'])
def y_predict():
    
    Pregnancies = request.form["Pregnancies"]
    Glucose = request.form["Glucose"]
    BloodPressure = request.form["BloodPressure"]
    SkinThickness = request.form["SkinThickness"]
    Insulin = request.form["Insulin"]
   
    BMI = request.form["BMI"]
    DiabetesPedigreeFunction = request.form["DiabetesPedigreeFunction"]
    Age = request.form["Age"]


    t = [[int(Pregnancies),int(Glucose),int(BloodPressure),int(SkinThickness),int(Insulin),float(BMI),float(DiabetesPedigreeFunction),int(Age)]]
    print(t)
    payload_scoring = {"input_data": [ {"field": [["Pregnancies","Glucose","BloodPressure","SkinThickness","Insulin","BMI","DiabetesPedigreeFunction","Age"]],
                   "values": t}]}
    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/d9a94283-a920-46b3-9e39-33ae37844f93/predictions?version=2021-02-09', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    print(predictions)
    pred = predictions['predictions'][0]['values'][0][0]
    if(pred == 0):
        output = "Negative Diabetes"
        print("Negative Diabetes")
    else:
        output = "Positive Diabetes"
        print("Positive Diabetes")
    return render_template('index.html', prediction_text= output)


if __name__ == "__main__":
    app.run(debug=True)
