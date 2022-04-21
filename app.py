# import pickle
from flask import Flask, render_template, request
import requests, json
from joblib import load
import pickle
# from model import sc

fName1 = 'modelCr.pkl'
modelCr = pickle.load(open(fName1, 'rb'))



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/call_weather')
def call_weather():
    return render_template('index.html', predictionW='form')


@app.route('/get_weather', methods=['POST'])
def get_weather():
    cName = str(request.form['City'])
    api_key = "516b385972ffc07a66437095d39ab15d"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + cName

    response = requests.get(complete_url)
    x = response.json()

    if x["cod"] != "404":
        y = x["main"]

        temp = round( (y["temp"] - 273.15), 2 )
        humidity = y["humidity"]


        return render_template('index.html', predictionT=temp, predictionH=humidity)
    else:
        return None




@app.route('/predict', methods=['POST'])
def predict():
    nitrogen = int(request.form['n'])
    phosporous = int(request.form['p'])
    potassium = int(request.form['k'])
    temperature = float(request.form['temp'])
    humidity = float(request.form['h'])
    phValue = float(request.form['ph'])
    rainfall = float(request.form['rain'])

    inputsCr = [nitrogen, phosporous, potassium, temperature, humidity, phValue, rainfall]
    crop_suggestion = int(modelCr.predict([inputsCr]))
    

    label = ['apple', 'banana', 'blackgram', 'chickpea', 'coconut', 'coffee', 'cotton',
             'grapes', 'jute', 'kidneybeans', 'lentil', 'maize', 'mango', 'mothbeans',
             'mungbean', 'muskmelon', 'orange', 'papaya', 'pigeonpeas', 'pomegranate',
             'rice', 'watermelon']
    # print(label[soil_fertility-1])


    return render_template('index.html', predictionCr=label[crop_suggestion-1])


if __name__ == "__main__":
    app.run(debug=True)
