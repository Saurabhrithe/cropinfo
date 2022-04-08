from flask import Flask, render_template, request
# import pickle
# import numpy as np
import pickle

fName = 'modelCr.pkl'
model = pickle.load(open(fName, 'rb'))



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    nitrogen = int(request.form['n'])
    phosporous = int(request.form['p'])
    potassium = int(request.form['k'])
    temperature = float(request.form['temp'])
    humidity = float(request.form['h'])
    phValue = float(request.form['ph'])
    rainfall = float(request.form['rain'])

    inputs = [[nitrogen, phosporous, potassium, temperature, humidity, phValue, rainfall]]


    pre = int(model.predict(inputs))

    teams = {
        1: 'Kolkata Knight Riders', 2: 'Chennai Super Kings', 3: 'Rajasthan Royals', 4: 'Mumbai Indians',
        5: 'Kings XI Punjab', 6: 'Royal Challengers Bangalore', 7: 'Delhi Daredevils', 8: 'Sunrisers Hyderabad'
    }

    return render_template('index.html', prediction=pre)


if __name__ == "__main__":
    app.run(debug=True)