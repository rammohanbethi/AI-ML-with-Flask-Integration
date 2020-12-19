import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle
import requests
import urllib3, json
url     = "https://iam.bluemix.net/oidc/token"
headers = { "Content-Type" : "application/x-www-form-urlencoded" }
data    = "apikey=" + '9iuENwY0YhJozrWGVgv_kkE1qg2a9KqMIRvEY7U8gKYl' + "&grant_type=urn:ibm:params:oauth:grant-type:apikey"
IBM_cloud_IAM_uid = "bx"
IBM_cloud_IAM_pwd = "bx"

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/y_predict',methods=['POST'])
def y_predict():
    x_test = [[int(x) for x in request.form.values()]]
    response  = requests.post( url, headers=headers, data=data, auth=( IBM_cloud_IAM_uid, IBM_cloud_IAM_pwd ) )
    print(response)
    iam_token = response.json()["access_token"]
    header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + iam_token, 'ML-Instance-ID': '4a15d5e4-69e9-4b45-91b3-d083431b27a5'}

# NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": ["YearsExperience"], "values": x_test}]}
    response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/v4/deployments/54a39efa-acfe-40e3-8b37-b55eae8bf1bb/predictions', json=payload_scoring, headers=header)
    #print(response_scoring)
    a = json.loads(response_scoring.text)
    pred = a['predictions'][0]['values'][0][0]
    return render_template('index.html', prediction_text='Predicted Salary is '+str(pred))


if __name__ == "__main__":
    app.run(debug=True)
