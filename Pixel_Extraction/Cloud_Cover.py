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
prefix = "https://www.windy.com/-Low-clouds-lclouds?lclouds"
suffix = "m:evxaifK"
latitude = 14.294478
longitude = 77.404746
zoom_level = 8

driver.get(prefix + ',' + str(latitude) + ',' + str(longitude) + ',' + str(zoom_level) + ',' + suffix)

""" Search locations on Windy & Wait until search box is created """
lat_long_search = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "q")))
lat_long_search.send_keys(str(latitude), ",", str(longitude))

""" Press Enter for the Search to happen """
temp = is_element_exist(driver, '#detail > div.closing-x')

while not temp:
    temp = is_element_exist(driver, '#detail > div.closing-x')
    lat_long_search.send_keys(Keys.ENTER)

""" Press Red Cross occur after search """
sleep(1)
WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#detail > div.closing-x"))).click()

""" Selector for value of all tags"""
title_value_selector = '#map-container > div.leaflet-pane.leaflet-map-pane > div.leaflet-pane.leaflet-marker-pane > div.leaflet-marker-icon.picker.open.leaflet-zoom-animated.leaflet-interactive.leaflet-marker-draggable > div.picker-content.noselect > span > big'

""" Low Cloud Tag """
# low cloud by default selected so no need to check for it
low_cloud_button_selector = '#overlay > a:nth-child(13) > div.menu-text.noselect.notap'   # low cloud by default selected
if is_element_exist(driver, title_value_selector):
    low_cloud_value = driver.find_element_by_css_selector(title_value_selector).get_attribute("innerHTML").splitlines()[0]

""" Cloud tag click and value extraction """
cloud_button_selector = '#overlay > a:nth-child(12) > div.menu-text.noselect.notap'
WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, cloud_button_selector))).click()
sleep(1)
if is_element_exist(driver, title_value_selector):
    cloud_value = driver.find_element_by_css_selector(title_value_selector).get_attribute("innerHTML").splitlines()[0]


""" Open Multiple Tag Option to get high and medium cloud cover """
layer = "#ovr-menu > div.iconfont.noselect.notap"
driver.find_element_by_css_selector(layer).click()

""" High Cloud tag click and value extraction """
high_cloud_button_selector = '#plugin-overlays > div.plugin-content > nav > a:nth-child(17) > span'
WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, high_cloud_button_selector))).click()
sleep(1)
if is_element_exist(driver, title_value_selector):
    high_cloud_value = driver.find_element_by_css_selector(title_value_selector).get_attribute("innerHTML").splitlines()[0]

""" Medium Cloud tag click and value extraction """
medium_cloud_button_selector = '#plugin-overlays > div.plugin-content > nav > a:nth-child(18) > span'
WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, medium_cloud_button_selector))).click()
sleep(1)
if is_element_exist(driver, title_value_selector):
    medium_cloud_value = driver.find_element_by_css_selector(title_value_selector).get_attribute("innerHTML").splitlines()[0]





from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

# create action chain object
action = ActionChains(driver)

# perform the operation
action.key_down(Keys.CONTROL).send_keys('ARROW_RIGHT').key_up(Keys.CONTROL).perform()
action.key_down(Keys.CONTROL).send_keys('ARROW_UP').key_up(Keys.CONTROL).perform()

