import smtplib
import requests
from decouple import config

OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/onecall"
MY_EMAIL = config("MY_EMAIL")
MY_PASSWORD = config("MY_PASSWORD")
API_KEY = config("OWM_API_KEY")

weather_params = {
    "lat": 19.4249946,
    "lon": -99.1649835,
    "appid": API_KEY,
    "exclude": "current,minutely,daily,alerts"
}

response = requests.get(OWM_ENDPOINT, params=weather_params)
response.raise_for_status()
weather_data = response.json()

weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
       will_rain = True

def send_message(body_message, final_sentence):
    with smtplib.SMTP("smtp.gmail.com", port = 587) as connection:
        connection.starttls()
        connection.login(user = MY_EMAIL, password = MY_PASSWORD)
        connection.sendmail(
            from_addr = MY_EMAIL, 
            to_addrs = MY_EMAIL, 
            msg = f"Subject:Condición Meteorológica\n\n{body_message}\n\n{final_sentence}".encode('utf-8').strip()
        )

if will_rain:
    send_message('Yo del futuro asegurate de llevar paraguas porque puede que hoy llueva en la CDMX.')
else:
    send_message('Al parecer no lloverá aunque no estaría de más llevar algún sueter.')
