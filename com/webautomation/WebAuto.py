from selenium.webdriver.common.keys import Keys
from pathlib import Path
from selenium import webdriver
import time, json, requests
import matplotlib.pyplot as plt
import os

# START: Variables declaration
chropath = "C:\\temp\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chropath)
url = "https://weather.com/"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
API_KEY = "1f11b1e1b9e3b8b4596a512d202cc5fa"
CITY_GRAPH = []
TEMP = []
outputFileName = "Output.txt"
# END: Variables declaration

my_file = Path(os.getcwd() + "\\" + outputFileName)
if my_file.exists():
    del my_file
oFile = open(outputFileName, 'w')

# This method fetch the temperature value of different cities from the URL
def getTemperatureFromUI(city):
    driver.get(url)
    driver.maximize_window()
    time.sleep(8)
    element = driver.find_element_by_xpath("//input[@id='LocationSearch_input']")
    element.clear()
    element.send_keys(city)
    time.sleep(2)
    driver.find_element_by_xpath("//button[@id='LocationSearch_listbox-0']").click()
    time.sleep(8)
    dummy = driver.find_element_by_xpath(
        "//body/div[@id='appWrapper']/main[@id='MainContent']/div[2]/main[1]/div[1]/div[1]/section[1]/div[1]/div[2]/div[1]/span[1]").text
    temp = str(dummy)
    return int(temp[:-1])

# This method fetches the value of different cities with the help of API
def getTemperatureFromAPI(city):
    URL = BASE_URL + "q=" + city + "&units=metric" + "&appid=" + API_KEY
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        temperatureUsingAPI = main['temp']
        TEMP.append(temperatureUsingAPI)
        CITY_GRAPH.append(CITY[i])
    else:
        print("HTTP request error")
    return temperatureUsingAPI

# Execution starts from here
if __name__ == "__main__":
    try:
        file = open('data.json', 'r')
        data = json.load(file)

        for i in data['Weather']:
            CITY = i['City']
            city_len = len(i['City'])
            Variance = i['Variance']
            if city_len != 0 and Variance is not None:
                for i in range(city_len):
                    temperatureFromUI = getTemperatureFromUI(CITY[i])
                    temperatureUsingAPI = getTemperatureFromAPI(CITY[i])
                    if 0 <= abs(temperatureFromUI - temperatureUsingAPI) <= Variance:
                        oFile.write("SUCCESS: " + CITY[i] + " temperature is in specified variance range" + "\n")
                        oFile.flush()
                    else:
                        oFile.write("MATCHER EXCEPTION: " + CITY[i] + " temperature is not in specified variance range" + "\n")
                        oFile.flush()
            else:
                print("Please enter valid data in input file")
    except FileNotFoundError:
        print("File Not Found")
    finally:
        file.close()
        driver.close()

    # Creating a graph to demonstrate the temperature vs city using the values fetched by hitting the API for different cities

    plt.bar(list(dict.fromkeys(CITY_GRAPH)), TEMP)
    plt.xlabel("City")
    plt.ylabel("Temperature (°C)")
    plt.title("Weather Report")
    plt.show()