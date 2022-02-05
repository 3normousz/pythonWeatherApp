import tkinter as tk
from PIL import Image, ImageTk
import datetime
import requests
import urllib.request
import io

LARGE_FONT = ('Verdana', 12)
LARGE_BOLD_FONT = ('Verdana', 12, "bold")
MEDIUM_FONT = ('Verdana', 10)
SEABLUE = "#Aab2b5"

class WebImage:
    def __init__(self, url):
        with urllib.request.urlopen(url) as u:
            raw_data = u.read()
        # self.image = tk.PhotoImage(data=base64.encodebytes(raw_data))
        image = Image.open(io.BytesIO(raw_data))
        self.image = ImageTk.PhotoImage(image)

    def get(self):
        return self.image


class App:

    def get_date(self, timezone):
        tz = datetime.timezone(datetime.timedelta(seconds=int(timezone)))
        return datetime.datetime.now(tz=tz).strftime(
            "%B %d, %H:%M:%S")  # strftime is just for visually formatting the datetime object

    def __init__(self):
        self.app = tk.Tk()
        self.app.title("Weather")
        self.app.geometry("700x350")
        self.app.resizable(0, 0)
        self.app.configure(bg=SEABLUE)

        self.user_input = tk.StringVar()
        self.api_key = '//PUT YOUR API KEY//'

        self.city_input = tk.Entry(self.app, textvariable=self.user_input, font=LARGE_FONT)
        self.city_input.insert(0, 'Enter a city name')
        self.city_input.bind("<FocusIn>", lambda args: self.city_input.delete('0', 'end'))
        self.city_input.pack(pady=8)

        self.search_button = tk.Button(self.app, text="Search", command=lambda: self.search_city(), font=MEDIUM_FONT)
        self.search_button.pack(pady=2)

        ##### COUNTRY CODE
        self.country = tk.Label(self.app, anchor=tk.CENTER, bg=SEABLUE, font=MEDIUM_FONT)
        self.country.pack(pady=8)
        ##### TIME WIDGET
        self.time = tk.Label(self.app, anchor=tk.CENTER, bg=SEABLUE, font=MEDIUM_FONT)
        self.time.pack()
        ##### PHOTO IMAGE
        self.imagelab = tk.Label(self.app, bg=SEABLUE)
        self.imagelab.pack()

        self.city_temp = tk.Label(self.app, anchor=tk.CENTER, bg=SEABLUE, font=LARGE_BOLD_FONT)
        self.city_temp.pack()
        ##### WEATHER WIDGET
        #self.city_weather = tk.Label(self.app, anchor=tk.CENTER, bg=SEABLUE)
        #self.city_weather.pack()

        self.city_feels_like = tk.Label(self.app, anchor=tk.CENTER, bg=SEABLUE, font=MEDIUM_FONT)
        self.city_feels_like.pack()

        self.city_weather_description = tk.Label(self.app, anchor=tk.CENTER, bg=SEABLUE, font=MEDIUM_FONT)
        self.city_weather_description.pack()


        self.city_wind = tk.Label(self.app, anchor=tk.CENTER, bg=SEABLUE, font=MEDIUM_FONT)
        self.city_wind.pack()

        self.city_sunrise = tk.Label(self.app, anchor=tk.CENTER, bg=SEABLUE, font=MEDIUM_FONT)
        self.city_sunrise.pack()

    def search_city(self):
        self.weather_data = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?q={self.user_input.get()}&units=metric&APPID={self.api_key}")

        if self.weather_data.json()['cod'] == '404':
            self.country.config(text="No City Found")

            self.time.config(text="")
            self.imagelab.config(image="")
            self.city_weather_description.config(text="")
            self.city_temp.config(text="")
            self.city_feels_like.config(text="")
            self.city_wind.config(text="")

        else:
            self.countrycode = self.weather_data.json()['sys']['country']
            self.weather = self.weather_data.json()['weather'][0]['main']
            self.weather_description = self.weather_data.json()['weather'][0]['description']
            self.icon_id = self.weather_data.json()['weather'][0]['icon']
            self.link = f"http://openweathermap.org/img/wn/" + self.icon_id + "@2x.png"
            self.temp = round(self.weather_data.json()['main']['temp'])
            self.feels_like = round(self.weather_data.json()['main']['feels_like'])
            self.wind = round(self.weather_data.json()['wind']['speed'] * 3.6)
            self.timezone = self.weather_data.json()['timezone']

            ##### COUNTRY CODE
            self.country.config(text=f"{self.user_input.get() + ',' + ' ' + self.countrycode}")

            ##### TIME WIDGET
            self.time.config(text=f"{self.get_date(self.timezone)}")

            ##### PHOTO WIDGET
            self.photo()
            self.imagelab.config(image=self.img)

            ##### WEATHER WIDGET
            #self.city_weather.config(text=f"The weather in {self.user_input.get()} is : {self.weather}")
            self.city_weather_description.config(text=f"Condition {self.weather_description}")

            self.city_temp.config(text=f"{self.temp}ºC")

            self.city_feels_like.config(text=f"Feels like : {self.feels_like}ºC")

            self.city_wind.config(text=f"Wind speed {self.wind} km/h")

    def photo(self):
        self.img = WebImage(self.link).get()

    def run(self):
        self.app.mainloop()


if __name__ == "__main__":
    myApp = App()
    myApp.run()
