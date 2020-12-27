from flask import Flask, render_template, request
import requests
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message


def convertUnix(unixtime):
    return(datetime.utcfromtimestamp(unixtime))


app = Flask(__name__)
app.config['DEBUG'] = True

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'emarza975@gmail.com',
    MAIL_PASSWORD = 'pqwwgovtakywwzvh',
)
app.config.from_object(__name__)
mail = Mail(app)

@app.route('/')
def index():
    # i.e. https://api.openweathermap.org/data/2.5/onecall?lat=45.42301&lon=12.03012&exclude=current,minutely,hourly,alerts&appid=a5ecab4555fcb510a356ed6f2413937e&units=metrics&lang=it
    API_key = 'a5ecab4555fcb510a356ed6f2413937e'
    lat = 45.42
    lon = 12.03
    part ='current,minutely,hourly,alerts'
    # [optional] By using this parameter you can exclude some parts of the weather data from the API response. It should be a comma-delimited list (without spaces). Available values: current, minutely, hourly, daily, alerts
    units = 'metric'
    # [optional] Units of measurement. standard, metric and imperial units are available. If you do not use the units parameter, standard units will be applied by default.
    lang = 'it'
    # [optional] language code
    url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}&appid={}&units={}&lang={}'
    r = requests.get(url.format(lat,lon,part,API_key,units,lang)).json()
    print(r)

    weather = {
        'lat' : lat,
        'lon' : lon,
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


    weather_str = """
    <table>
            <tr>
            <td>    Data </td>
            <td>    Previsione </td>
            <td>    Alba </td>
            <td>    Tramonto </td>
            <td>    Temp. Min. </td>
            <td>    Temp. Max</td>
            <td>    Pressione</td>
            <td>    Nuvoloso </td>
            <td>    Vento Vel. </td>
        </tr> """

    for i in range(8):
        weather_str += "<tr><td>" + weather['forecast'][i]['date'] + '</td><td><img src="http://openweathermap.org/img/w/'+weather['forecast'][i]['icon'] +'.png"alt="'+ weather['forecast'][i]['description'] +'"><br>'+ weather['forecast'][i]['description'] +' <td><td>'
        weather_str += str(weather['forecast'][i]['sunrise']) +' </td>'
        weather_str += '<td>'+ str(weather['forecast'][i]['sunset']) +' </td>'
        weather_str += '<td>'+ str(weather['forecast'][i]['temp_min']) +' °C </td>    <td>'+ str(weather['forecast'][i]['temp_max']) +' °C</td> '
        weather_str += '   <td>'+ str(weather['forecast'][i]['pressure']) +' mbar</td>    <td>'+ str(weather['forecast'][i]['clouds']) +' %</td>'
        weather_str += '    <td>'+ str(weather['forecast'][i]['wind_speed']) +' km/h</td></tr>'

    weather_str += '</table>'
    # print(weather)
    msg = Message("Previsioni meteo",
                  sender="emarza975@gmail",
                  recipients=['marianna.perale@gmail.com'],
                 html=weather_str)


    mail.send(msg)


    return render_template('weather.html', weather = weather)

@app.route('/send_mail', methods= ['POST'])
def send_mail():
    msg = Message("prova",
                  sender="emarza975@gmail",
                  recipients=[request.form['email']])


    mail.send(msg)
    return render_template('hello.html')
