import tkinter as tk
import requests
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap

root = ttkbootstrap.Window(themename="morph")
root.title("Weather App")
root.geometry("400x400")

# Function get weather information from OpenWeatherMap API
def get_weather(city):
    API_key = ""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_key}"
    res = requests.get(url)

    if res.status_code == 404:
        messagebox.showerror("Error","City not found")
        return None
    
    # Parse the response JSON to get weather information
    weather = res.json() # Converts the HTTP response to json
    icon_id = weather['weather'][0]['icon']
    temperature = weather['main']['temp'] - 273.15 # Converts it to celcius
    description=weather['weather'][0]['description']
    city = weather['name']
    country = weather['sys']['country']

    # Get the icon URL and return all the weather information
    icon_url = f"https://openweathermap.org/img/wn/{icon_id}@2x.png"
    return(icon_url,temperature,description,city,country)


# Function to search weather for a city
def search():
    city = city_name.get()
    result = get_weather(city)
    if result is None:
        return
    # If the city is found unpack weather information
    icon_url,temperature,description,city,country = result
    location_label.configure(text=f"{city}, {country}")

    # Get the weather icon image from URL and update the icon label
    image = Image.open(requests.get(icon_url, stream=True).raw)
    icon = ImageTk.PhotoImage(image)
    icon_label.configure(image=icon)
    icon_label.image = icon

    # Update the temperature and description labels
    temperature_label.configure(text=f"Temperature: {temperature:.2f}°C")
    description_label.configure(text=f"Description: {description}")

# Entry widget to enter the city name
city_name = ttkbootstrap.Entry(root, font= "Helvetica, 18")
city_name.pack(pady=10)

# Button widget to search for the weather information
search_button = ttkbootstrap.Button(root, text="Search", command=search, bootstyle="warning" )
search_button.pack(pady=10)

# Label widget to show city/country name
location_label = tk.Label(root, font="Helvetica, 25")
location_label.pack(pady=20)

# Label widget to show the weather icon
icon_label = tk.Label(root)
icon_label.pack()

# Label widget to show weather description
temperature_label = tk.Label(root, font="Helvetica, 20")
temperature_label.pack()

# Label widget to show weather description
description_label = tk.Label(root, font="Helvetica, 20")
description_label.pack()

root.mainloop()