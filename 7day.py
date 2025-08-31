import modules.trips
import os
import pyautogui
import shutil
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select #for selecting from dropdown
from selenium.webdriver.edge.service import Service #for disabling Chrome logging
from selenium.webdriver.support.ui import WebDriverWait #for waiting for elements to load
from selenium.webdriver.support import expected_conditions as EC #for waiting for elements to load
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from colorama import Fore, Style, init

init(autoreset=True)
company_code = modules.trips.company_code_input()
user_name = modules.trips.user_name_input()
password = modules.trips.password_input()

# WellRyde Login
service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service)

modules.trips.login_page(company_code, user_name, password, driver)
modules.trips.trip_tab_nav(driver)
print('Initial navigation to TRIP tab [', end='')
print(Fore.GREEN + 'SUCCESS', end='')
print(']')

modules.trips.weekly_trips(driver)
print('Initial navigation to seven day range page [', end='')
print(Fore.GREEN + 'SUCCESS', end='')
print(']')

modules.trips.process_rider_trips_weekly(driver)

driver.quit()
