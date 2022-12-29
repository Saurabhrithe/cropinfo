from flask import Flask, render_template, request
import pickle
import preprocessing as pre

fName1 = 'modelCr.pkl'
modelCr = pickle.load(open(fName1, 'rb'))

app = Flask(__name__)


@app.route('/call_W')
def call_W():
    return render_template('weather.html')


@app.route('/get_W', methods=['POST'])
def get_W():
    place = request.form['place']
    freq = str(request.form['options'])

    l, val3 = pre.load(place, freq)
    values1, values2, values3 = l[0], l[1], val3

    mx = round(max(max(values1), max(values2), max(values3)))
    t_min, t_max, feels_like, h = pre.live_weather(place)
    return render_template('weather.html', labels=l[2], values1=values1, values2=values2, values3=values3, place=place,
                            temp_min=t_min, temp_max=t_max, feels_like=feels_like, humidity=h, mx=mx)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/call_weather')
def call_weather():
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

    inputsCr = [nitrogen, phosporous, potassium, temperature, humidity, phValue, rainfall]
    crop_suggestion = int(modelCr.predict([inputsCr]))

    label = ['apple', 'banana', 'blackgram', 'chickpea', 'coconut', 'coffee', 'cotton',
             'grapes', 'jute', 'kidneybeans', 'lentil', 'maize', 'mango', 'mothbeans',
             'mungbean', 'muskmelon', 'orange', 'papaya', 'pigeonpeas', 'pomegranate',
             'rice', 'watermelon']

    return render_template('index.html', predictionCr=label[crop_suggestion-1])


if __name__ == "__main__":
    app.run(debug=True)
