import json
from sys import exit, argv
from expections import *
import requests
from tabulate import tabulate
from datetime import datetime, date
from art import *

def main():
    # open json file and read api key
    APIKEY = "5778ebef63827aa7fd5a136d866fd37d"
    
    # Getting user input handline input from command line OR user input
    arg_count = len(argv)
    if arg_count == 1:
        locationName = getLocation()
    elif arg_count == 2:
        locationName = argv[1]

        if not validateLocation(locationName):
            exit("Invalid Input")
    else:
        exit("Too many argument!")
    
    
    # Make network request
    try:
        data = make_request(locationName, APIKEY)
    except LocationNotFound:
        exit("Invalid location input, please try again with a valid location!")
    except:
        exit("Gets an unknown error while getting data")


    # Data cleaning
    sanitized_data = cleanData(data)

    # Printing Header
    printHeader(sanitized_data["City"])
    # Printing data table
    printToTable(sanitized_data, headers=["Data", "Value"])
    
   
    try:
        userChoice = input("Want to continue Y/N: ").lower()
        if userChoice == "y":
            print("Starting new session....")
            main()
        else:
            exit("Exiting....")
    except:
        exit("Exiting...")

    


# turning kelvin to celcius
def kelvinToCelcius(kelvin):
    return f'{round(kelvin - 273.15)}°C'

# Get date
def getDate(timestamp):
    dt = date.fromtimestamp(timestamp)
    return dt.strftime("%d %b")

# get time
def getTime(timestamp):
    dt = datetime.fromtimestamp(timestamp)
    return dt.strftime("%X")
    
def formatWindSpeed(floatNum):
    return f"{round(floatNum * 3.6)} km/h"

# Making network requests
def make_request(location, apikey):
    URL = "https://api.openweathermap.org/data/2.5/weather"
    response = requests.get(URL, {"q":location, "apikey": apikey})
    response = response.json()
    
    if response["cod"] == "404":
        raise LocationNotFound
    
    return response


# Cleanup messy data
def cleanData(rawdata):
    return {
        "Status": rawdata["weather"][0]["description"],
        "Tempreture": kelvinToCelcius(rawdata["main"]["temp"]),
        "Feels Like": kelvinToCelcius(rawdata["main"]["feels_like"]),
        "Min Temp": kelvinToCelcius(rawdata["main"]["temp_min"]),
        "Max Temp": kelvinToCelcius(rawdata["main"]["temp_max"]),
        "Pressure": rawdata["main"].get("pressure", 0),
        "Humidity": f'{rawdata["main"].get("humidity", 0)} %',
        "Sea Level": rawdata["main"].get("sea_level", 0),
        "Ground Level": rawdata["main"].get("grnd_level", 0),
        "Visibility": f'{round(rawdata["visibility"] / 100)} %',
        "Wind Speed": formatWindSpeed(rawdata["wind"].get("speed", 0)),
        "Clouds": f'{rawdata["clouds"]["all"]} %',
        "Date": getDate(rawdata["dt"]),  
        "Sunrise": getTime(rawdata["sys"]["sunrise"]),
        "Sunset": getTime(rawdata["sys"]["sunset"]),
        "City": rawdata["name"],
        "Country": rawdata["sys"]["country"]
    }
    

# HELPER FUNCTIONS
    
# output data as table
def printToTable(data, headers, format = "psql"):
    dataList = data.items()
    print(tabulate(dataList, headers=headers, tablefmt=format))
    
# Print Header
def printHeader(cityName):
    city = cityName.upper()    
    print(city)
    Art=text2art(city,font='block',chr_ignore=True)
    print(Art)
    # print(pyfiglet.Figlet("banner3-D").renderText(city), end="")

# Get user input   
def getLocation():
    while True:
        try:
            location = input("Location Name: ").lower()
            
            if validateLocation(location):
                return location
            else:
                pass
        except KeyboardInterrupt:
            exit("Exiting...")

# CHecking validation
def validateLocation(location):
    return location and location.isalpha()    



if __name__ == "__main__":
    main()