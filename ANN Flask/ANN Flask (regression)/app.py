import numpy as np
from flask import Flask, request, jsonify, render_template
from joblib import load
from tensorflow.keras.models import load_model
app = Flask(__name__)
model = load_model("regression.h5")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/y_predict',methods=['POST'])
def y_predict():

    a = request.form['a']
    b = request.form['b']
    c = request.form['c']
    d = request.form['State']

    if (d == "New York"):
        s1,s2,s3 = 0,0,1
    if (d == "Florida"):
        s1,s2,s3 = 0,1,0
    if (d == "California"):
        s1,s2,s3 = 1,0,0

    total = [[s1,s2,s3,a,b,c]]
    total_1 = np.asarray(total, dtype='float64')
    #print(total_1)
    prediction = model.predict(total_1)
    output = np.round(prediction[0][0],3)
    #print(prediction)
    #output=prediction[0][0]
    
    return render_template('index.html', prediction_text='Profit {}'.format(output))

if __name__ == "__main__":
    app.run(debug=True)
