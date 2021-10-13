from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from PIL import Image
from io import BytesIO
import os
import cv2 as cv
import numpy as np


def is_element_exist(chrome_driver, locator):
    try:
        chrome_driver.find_element_by_css_selector(locator)
        return True
    except NoSuchElementException:
        return False


""" Create driver for particular web browser """
driver = webdriver.Chrome(executable_path='/home/kanav/.config/spyder-py3/Drivers/chromedriver')
driver.maximize_window()

""" Windy Link """
prefix = "https://www.windy.com/-Satellite-satellite?satellite"
suffix = "m:evxaifK"


def radiation_pixel(latitude, longitude, zoom_level, farm_name, parent_path, date_path, block_id, iteration, total_location):
    driver.get(prefix + ',' + str(latitude) + ',' + str(longitude) + ',' + str(zoom_level) + ',' + suffix)

    """ Search locations on Windy & Wait until search box is created """
    lat_long_search = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "q")))
    lat_long_search.send_keys(str(latitude), ",", str(longitude))

    """ Press Enter for the Search to happen """
    temp = is_element_exist(driver, '#detail > div.closing-x')

    while not temp:
        temp = is_element_exist(driver, '#detail > div.closing-x')
        lat_long_search.send_keys(Keys.ENTER)

    """ Get coordinates of locations pinned """
    loc_pin = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                         "#map-container > div.leaflet-pane.leaflet-map-pane > div.leaflet-pane.leaflet-marker-pane > div.leaflet-marker-icon.picker.open.leaflet-zoom-animated.leaflet-interactive.leaflet-marker-draggable > div.picker-lines.noselect")))
    location = loc_pin.location

    """ Get pinned tag removed from location """
    sleep(.5)
    loc_tag = WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                         "#map-container > div.leaflet-pane.leaflet-map-pane > div.leaflet-pane.leaflet-marker-pane > div.leaflet-marker-icon.picker.open.leaflet-zoom-animated.leaflet-interactive.leaflet-marker-draggable > div.picker-content.noselect > a.picker-close-button.shy")))
    loc_tag.click()

    """ Press Red Cross occur after search """
    WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#detail > div.closing-x"))).click()
    sleep(1)

    """ Take screenshot and save it """
    png = driver.get_screenshot_as_png()

    im = Image.open(BytesIO(png))  # uses PIL library to open image in memory
    left = location['x'] - 160
    top = location['y'] - 33
    right = location['x'] + 175
    bottom = location['y'] + 280
    im = im.crop((left, top, right, bottom))  # defines crop points

    """ Path creation and saving screenshot in it """
    image_path = parent_path + "/Images/" + date_path
    if not os.path.exists(image_path):
        os.makedirs(image_path)
        print("Path Created: ", image_path)
    else:
        print("Path already exists: ", image_path)

    image_name = image_path + "/" + str(farm_name) + ".png"
    im.save(image_name)  # saves new cropped image

    """ Read the screenshots and return there pixel value"""
    image = cv.imread(image_path + "/" + farm_name + ".png")
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    pixel_value = round(np.mean(image), 2)

    pixel_dict = {
        'Block_Id': block_id,
        'Farm_Name': farm_name,
        'Pixel_Value': pixel_value
    }

    if iteration == total_location:
        driver.quit()

    return pixel_dict

