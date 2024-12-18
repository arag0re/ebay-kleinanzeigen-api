from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

from functions.getProxy import *
from functions.getUserAgent import *

import logging
logging.basicConfig(level=logging.DEBUG)

def scrapeInserateUrls(
    brand,
    model,
    type_,
    shiftType,
    hu,
    fuelType,
    powerFrom,
    powerTo,
    ezFrom,
    ezTo,
    kmFrom,
    kmTo,
    priceFrom,
    priceTo,
    unlistedCarModel,   # unlistedCarModel means that kleinanzeigen dont got a category specifically for this model
):                      # so we need to use the searchengine
    chrome_driver_path = "/usr/local/bin/chromedriver"
    driver = None
    try:
        start_time = time.time()

        proxy = getProxy()

        ez = "" # Erstzulassung
        km = ""
        _type_ = ""
        shiftTypeStr = ""
        huStr = ""
        power = ""
        price = ""
        fuel  = ""
        modelStr = ""
        unlistedCarModelStr = ""

        url = "https://www.kleinanzeigen.de/s-autos/"

        if ezFrom or ezTo:
            ez = f"+autos.ez_i:{ezFrom}%2C{ezTo}"

        if kmFrom or kmTo:
            km = f"+autos.km_i:{kmFrom}%2C{kmTo}"

        if priceFrom or priceTo:
            price = f"preis:{priceFrom}:{priceTo}/"

        if type_: # Cabrio, Kombi, etc
            _type_ = f"+autos.typ_s:{type_}"

        if shiftType:  # automatik & manuell
            shiftTypeStr = f"+autos.shift_s:{shiftType}"

        if hu: # Jahreszahl bis wann TÜV
            huStr = f"+autos.tuevy_i:{hu}%2C"

        if fuelType: # diesel, benzin, gas, elektro?
            fuel = f"+autos.fuel_s:{fuelType}"

        if powerFrom or powerTo:
            power = f"+autos.power_i:{powerFrom}%2C{powerTo}"

        if unlistedCarModel:
            unlistedCarModelStr = unlistedCarModel.replace(" ", "-")                                                            # If unlistedCarModel is set we dont add a brand or model into the url
            unlistedCarModelStr = f"{unlistedCarModelStr}/k0"  # We use the searchengine for unlistedCarModels

        if brand: # like Volkeswagen
            if model: # i.e. Golf
                modelStr = f"+autos.model_s:{model}"
            url += f"{brand}/{price}{unlistedCarModelStr}c216{ez}{fuel}{km}+autos.marke_s:{brand}{modelStr}{power}{shiftTypeStr}{huStr}{_type_}" # Brand, Model and Type are logically attached, cause not every model is available from every brand. Also not every model is available in any type.
        else:
            url += f"{price}{unlistedCarModelStr}c216{ez}{fuel}{km}{power}{shiftTypeStr}{huStr}{huStr}{_type_}"

        logging.debug(f"URL: {url}")  # Log the result
        prox_options = {"proxy": {"http": proxy}}

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--user-agent=" + GET_UA())
        options.add_argument("--incognito")
        driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)

        driver.get(url)

        elements = driver.find_elements(By.CLASS_NAME, "aditem")
        urlArray = []
        for element in elements:
            urlArray.append(
                "https://www.kleinanzeigen.de" + element.get_attribute("data-href")
            )

        data = {"urls": urlArray}

        end_time = time.time()
        # print("Scraped "+str(len(urlArray))+" urls")
        print("scrapeInserate.py execution:")
        print(str(round(end_time - start_time, 2)) + " seconds")
        print("Proxy: " + proxy)
        driver.quit()
        return data
    except Exception as e:
        print(e)
        driver.quit()
        return None
