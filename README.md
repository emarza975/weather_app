# **Weather App**
a simple web app for weather forecast (in Italian)

***
_for educational purposes only_

In this very simple web-app, I access data from [Open Weather Map API](https://openweathermap.org) and I can insert or delete cities from everywhere in the world.
For each city I can see a 7 days forecast (in a separate page).

[Let's go here for trying it!](http://lele75sp.pythoneverywhere.com)
***
#### _**USED MODULES**_
- [**Flask**](https://flask.palletsprojects.com/en/1.1.x/) (Flask, render_template, redirect,request, url_for)
- [**Flask alchemy**](https://www.sqlalchemy.org/) (SQLAlchemy)
- **flask-dotenv**
- **os** (environ)
- **requests**
- **datetime**


***
#### _**FILES**_
- weather2.py : engine code
- weather.db  : Sqlite3 Database with table cities
- weather_app.html : main homepage
- weather.html : 7 days forecast page



***
#### _**LIST VERSIONS**_

v. 1.0 (2020-12-26): completed engine - There's a minimal graphic interface. No CSS, I used [Bulma](https://bulma.io)
