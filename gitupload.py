import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import pandas as pd

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-logging"])
#1
options.binary_location = "F:\webdrive\chrome-win64\chrome-win64\\chrome.exe"   #change to your location 
#2
PATH = r'F:\webdrive\chromedriver.exe' #change also to your location
service = webdriver.chrome.service.Service(PATH)
driver = webdriver.Chrome(service=service, options=options)

def split_data(entry):
    # Split the entry by comma to separate title from other details
    title, details = entry.split(',', 1)

    # Extract individual components from details
#3
    price = details.split('cena:')[1].split('zł')[0].strip() + 'zł'  # Extract price #you can have other value so you probalby have to change zl to value that is in your country
    brand = details.split('marka:')[1].split(',')[0].strip()  # Extract brand
    size = details.split('rozmiar:')[1].strip()  # Extract size

    return title.strip(), price, brand, size
data = []

x =input("Search text : ")
x.replace(" ","%20")
p1=int(input("Number of pages :"))

for p in range(1,p1+1):
    driver.get(f"https://www.vinted.pl/catalog?search_text={x}&page={p}")
    time.sleep(2)
    try:
        cookie = driver.find_element(By.ID, "onetrust-accept-btn-handler")
        cookie.click()
    except:
        print("")
    products = driver.find_elements(By.CLASS_NAME, "new-item-box__overlay")


    for product in products:
        title = product.get_attribute("title")
        link = product.get_attribute("href")
        components = split_data(title)

        # Append the data to the list
        data.append({
            "Title": components[0],
            "Price": components[1],
            "Brand": components[2],
            "Size": components[3],
            "Link": link
        })

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(data)

    # Save the DataFrame to an Excel file
#4
    excel_filename = f"F:\pobrane nowe\pythek\webscraping uporządkowany\PROJEKT 6\{x}.xlsx" #zmiana lokacji zapisu pliku
    df.to_excel(excel_filename, index=False)

    print("Data exported to:", excel_filename)

#time.sleep(10000)