import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 42.697708
MY_LONG = 23.321867
MY_EMAIL = 'dilyana.m.bodurova@gmail.com'
MY_PASSWORD = 'my password'

def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True
    return False


def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response_curr_time = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response_curr_time.raise_for_status()
    data = response_curr_time.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True
    return False


while True:
    time.sleep(60)
    if is_iss_overhead() and is_dark():
        with smtplib.SMTP('smtp.gmail.com') as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL,
                                msg='Subject:Look up!\n\nThe iss is above you in the sky.')
