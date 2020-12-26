

weather = {'lat': 45.42, 'lon': 12.03, 'forecast': [{'date': '20-12-2020', 'sunrise': '06:48', 'sunset': '15:30', 'description': 'CIELO COPERTO', 'icon': '04d', 'temp_min': 6.62, 'temp_max': 9.07, 'pressure': 1025, 'wind_speed': 1.6, 'clouds': 100}, {'date': '21-12-2020', 'sunrise': '06:48', 'sunset': '15:31', 'description': 'NUBI SPARSE', 'icon': '04d', 'temp_min': 6.57, 'temp_max': 10.36, 'pressure': 1026, 'wind_speed': 1.74, 'clouds': 83}, {'date': '22-12-2020', 'sunrise': '06:49', 'sunset': '15:31', 'description': 'NUBI SPARSE', 'icon': '04d', 'temp_min': 5.98, 'temp_max': 9.76, 'pressure': 1026, 'wind_speed': 0.67, 'clouds': 76}, {'date': '23-12-2020', 'sunrise': '06:49', 'sunset': '15:32', 'description': 'CIELO COPERTO', 'icon': '04d', 'temp_min': 5.08, 'temp_max': 8.49, 'pressure': 1026, 'wind_speed': 0.66, 'clouds': 98}, {'date': '24-12-2020', 'sunrise': '06:50', 'sunset': '15:33', 'description': 'PIOGGIA LEGGERA', 'icon': '10d', 'temp_min': 6.49, 'temp_max': 6.9, 'pressure': 1015, 'wind_speed': 1.17, 'clouds': 100}, {'date': '25-12-2020', 'sunrise': '06:50', 'sunset': '15:33', 'description': 'PIOGGIA LEGGERA', 'icon': '10d', 'temp_min': 5.88, 'temp_max': 7.59, 'pressure': 1010, 'wind_speed': 4.58, 'clouds': 99}, {'date': '26-12-2020', 'sunrise': '06:50', 'sunset': '15:34', 'description': 'CIELO SERENO', 'icon': '01d', 'temp_min': 2.08, 'temp_max': 6.22, 'pressure': 1023, 'wind_speed': 1.05, 'clouds': 0}, {'date': '27-12-2020', 'sunrise': '06:51', 'sunset': '15:34', 'description': 'CIELO SERENO', 'icon': '01d', 'temp_min': 0.57, 'temp_max': 4.64, 'pressure': 1018, 'wind_speed': 0.84, 'clouds': 10}]}

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

for i in range(6):
    weather_str += "<tr><td>" + weather['forecast'][i]['date'] + '</td><td><img src="http://openweathermap.org/img/w/'+weather['forecast'][i]['icon'] +'.png"alt="'+ weather['forecast'][i]['description'] +'"><br>'+ weather['forecast'][i]['description'] +' <td><td>'
    weather_str += str(weather['forecast'][i]['sunrise']) +' </td>'
    weather_str += '<td>'+ str(weather['forecast'][i]['sunset']) +' </td>'
    weather_str += '<td>'+ str(weather['forecast'][i]['temp_min']) +' °C </td>    <td>'+ str(weather['forecast'][i]['temp_max']) +' °C</td> '
    weather_str += '   <td>'+ str(weather['forecast'][i]['pressure']) +' mbar</td>    <td>'+ str(weather['forecast'][i]['clouds']) +' %</td>'
    weather_str += '    <td>'+ str(weather['forecast'][i]['wind_speed']) +' km/h</td></tr>'

weather_str += '</table>'

print (weather_str)
