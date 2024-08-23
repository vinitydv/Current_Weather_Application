from flask import Flask, render_template, request
import requests
import datetime
import geocoder

app = Flask(__name__)


def get_temp(location):
    api_key = 'fd4990f3b8581815656c8049597e35e1'
    url = f"https://api.openweathermap.org/data/2.5/weather?"
    
    d = {
        'q':location,
        'appid':api_key,
        'units': 'metric'
        }
    
    resp = requests.get(url, params=d)
    if resp.status_code == 200:
        data = resp.json()
        temp = data['main']['temp']
        cloud = data['clouds']['all']
        humidity = data['main']['humidity']
        wind = data['wind']['speed']
        Type = data['weather'][0]['main']
        time = datetime.datetime.now().strftime('%H:%M')
        day_date = datetime.date.today().strftime("%A, %d %B' %y")
        time_day_date = ' - '.join((time, day_date))

        dict1 = {
            'Temp':str(temp)+'\N{DEGREE SIGN}c',
            'Location':location.upper(),
            'Time_Day_Date':time_day_date,
            'Cloudy':str(cloud)+' %',
            'Humidity':str(humidity)+' %',
            'Wind':str(wind)+' meter/sec',
            'Type':Type
        }
    else:
        return None
    return dict1


@app.route('/')
def home():
    g = geocoder.ip('me')
    location = g[0].raw['city']
    data = get_temp(location)
    return render_template('index.html', dict1 = data)


@app.route('/weatherdata/', methods=['GET', 'POST'])
def weather_data():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        location = request.form.get('location')
        data = get_temp(location)
        return render_template('index.html', dict1=data)


app.run(host='localhost', port=5000, debug=True)