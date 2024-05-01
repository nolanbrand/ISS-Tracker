import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 29.760427  # Your latitude
MY_LONG = -95.369804  # Your longitude
TIME_ZONE = "America/Chicago"
MY_EMAIL = "email@gmail.com"
PASSWORD = "password123"

while True:
    def iss_in_range():
        response = requests.get(url="http://api.open-notify.org/iss-now.json")
        response.raise_for_status()
        data = response.json()

        iss_latitude = float(data["iss_position"]["latitude"])
        iss_longitude = float(data["iss_position"]["longitude"])

        if (iss_longitude + 5 >= MY_LAT >= iss_latitude - 5) and (iss_longitude + 5 >= MY_LONG >= iss_longitude - 5):
            return True
        else:
            return False


    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
        "tzid": TIME_ZONE
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now()

    if iss_in_range() and (time_now.hour >= sunset or time_now.hour <= sunrise):
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg="Subject:ISS Overhead!\n\nThe ISS is visible tonight at your location!"
            )

    time.sleep(60)

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.
