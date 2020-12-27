from flask import Flask, render_template, redirect,request, url_for
import requests
from flask_sqlalchemy import SQLAlchemy
from os import environ
from datetime import datetime

SECRET_KEY = environ.get('SECRET_KEY')
API_KEY = environ.get('API_KEY')

app = Flask(__name__)
app.config['DEBUG'] = True


app.config.from_object(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


def convertUnix(unixtime):
    return(datetime.utcfromtimestamp(unixtime))


class Cities(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return  self.city_name



@app.route('/', methods=['GET','POST'])
def index():
    err_msg = ''
    if request.method == 'POST':
        if request.form['city_name']:
            city_name = request.form['city_name']
            city_exists = Cities.query.filter_by(city_name=city_name).first()
            if not city_exists:
                newcity = Cities(city_name=city_name)
                db.session.add(newcity)
                db.session.commit()
            else:
                err_msg = "La città è già presente."
                print('WARNING!!!' ,err_msg)
        else:
            err_msg = "Inserire almeno una città"
            print ('ERRORE!!! ', err_msg)


    #extract from db Cities the record of names of cities
    cities = Cities.query.all()
    units = 'metric'
    # [optional] Units of measurement. standard, metric and imperial units are available. If you do not use the units parameter, standard units will be applied by default.
    lang = 'it'
    # [optional] language code
    data = []
    for city in cities:
        #call the api of Open Weather Map
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city.city_name}&appid={API_KEY}&&units={units}&lang={lang}'

        r = requests.get(url).json()
        status_r = r['cod']
        print (city, status_r, r)
        if status_r == 200:
            data_city = {
                'city':city,
                'country':r['sys']['country'],
                'lon':r['coord']['lon'],
                'lat':r['coord']['lat'],
                'description':r['weather'][0]['description'].upper(),
                'icon': r['weather'][0]['icon'],
                'temp_min':r['main']['temp_min'],
                'temp_max':r['main']['temp_max'],
                'pressure':r['main']['pressure'],
                'humidity':r['main']['humidity'],
                'wind_speed':r['wind']['speed'],
            }
            data.append(data_city)
        else:
            err_msg = "ERROR!!! la città {} non esiste. Errore restituito da OpenWeatherMap: {} - {}".format(city,status_r, r['message'])
            del_city = Cities.query.filter_by(city_name=city.city_name).first()
            print(del_city)
            db.session.delete(del_city)
            db.session.commit()

    return render_template('weather_app.html', data = data, err_msg = err_msg)

@app.route('/delete_city/<city>')
def delete_city (city):
        del_city = Cities.query.filter_by(city_name=city).first()
        print(del_city)
        db.session.delete(del_city)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/seven_days/city=<city>&lat=<lat>&lon=<lon>')
def seven_days (city,lat,lon):
    # i.e. https://api.openweathermap.org/data/2.5/onecall?lat=45.42301&lon=12.03012&exclude=current,minutely,hourly,alerts&appid=a5ecab4555fcb510a356ed6f2413937e&units=metrics&lang=it
    part ='current,minutely,hourly,alerts'
    # [optional] By using this parameter you can exclude some parts of the weather data from the API response. It should be a comma-delimited list (without spaces). Available values: current, minutely, hourly, daily, alerts
    units = 'metric'
    # [optional] Units of measurement. standard, metric and imperial units are available. If you do not use the units parameter, standard units will be applied by default.
    lang = 'it'
    # [optional] language code
    url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&appid={}&units={}&lang={}'
    print(lat,lon)
    r = requests.get(url.format(lat,lon,part,API_KEY,units,lang)).json()
    print(r)

    weather = {
        'lat' : lat,
        'lon' : lon,
        'city': city,
        'forecast':[{},{},{},{},{},{},{},{}]
        }

    for i in range(8):
        weather['forecast'][i]['date']= convertUnix(r['daily'][i]['dt']).strftime('%d-%m-%Y')
        weather['forecast'][i]['sunrise']=convertUnix(r['daily'][i]['sunrise']).strftime('%H:%M')
        weather['forecast'][i]['sunset']=convertUnix(r['daily'][i]['sunset']).strftime('%H:%M')
        weather['forecast'][i]['description']= r['daily'][i]['weather'][0]['description'].upper()
        weather['forecast'][i]['icon']= r['daily'][i]['weather'][0]['icon']
        weather['forecast'][i]['temp_min']= r['daily'][i]['temp']['min']
        weather['forecast'][i]['temp_max']=r['daily'][i]['temp']['max']
        weather['forecast'][i]['pressure']=r['daily'][i]['pressure']
        weather['forecast'][i]['wind_speed']=r['daily'][i]['wind_speed']
        weather['forecast'][i]['clouds']=r['daily'][i]['clouds']

    return render_template('weather.html', weather = weather)
