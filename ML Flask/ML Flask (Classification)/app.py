import numpy as np
from flask import Flask, request, jsonify, render_template
from joblib import load

app = Flask(__name__)

model = load("naive.save")
sc=load("transform.save")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/y_predict',methods=['POST'])
def y_predict():

    a = request.form['z']
    b = request.form['b']
    c = request.form['c']
    d = request.form['d']
    e = request.form['e']
    f = request.form['f']
    g = request.form['g']
    h = request.form['h']

    total = [[a,b,c,d,e,f,g,h]]
    prediction = model.predict(sc.transform(total))

    if(prediction==0):
        output = "Negative  Diabete"
    else:
        output="Positive  Diabetes"
    
    return render_template('index.html', prediction_text=output)

if __name__ == "__main__":
    app.run(debug=True)
