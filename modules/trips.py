import time
import os
import pyautogui
import shutil
import pyperclip
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select #for selecting from dropdown
from selenium.webdriver.edge.service import Service #for disabling Chrome logging
from selenium.webdriver.support.ui import WebDriverWait #for waiting for elements to load
from selenium.webdriver.support import expected_conditions as EC #for waiting for elements to load
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from datetime import datetime
from colorama import Fore, Style, init


def company_code_input():
    print('')
    print('')
    print(Fore.GREEN + 'Please enter your ModivCare provided Company code: ', end='') 
    company_code = input(Fore.YELLOW + '')
    for i in range(5):
        print('')
    return company_code 


def user_name_input():
    print('')
    print('')
    print(Fore.GREEN + 'Please enter your ModivCare provided user name: ', end='') 
    user_name = input(Fore.YELLOW + '')
    for i in range(5):
        print('')
    return user_name 


def password_input():
    print('')
    print('')
    print(Fore.GREEN + 'Please enter your password: ', end='') 
    password = input(Fore.YELLOW + '')
    for i in range(5):
        print('')
    return password


def login_page(company_code, user_name, password, driver):

    try:
        web_page_loading = 'Reaching Wellryde'
        driver.get('https://portal.app.wellryde.com')
        print(f'{web_page_loading} [', end='')
        print(Fore.GREEN + 'SUCCESS', end='')
        print(']')
    except Exception as e:
        print(f'{web_page_loading} [', end='')
        print(Fore.RED + 'FAILED')
        print(']')

    try:
        maximize_window = 'Maximizing window'
        driver.maximize_window()
        print(f'{maximize_window} [', end='')
        print(Fore.GREEN + 'SUCCESS', end='')
        print(']')
    except Exception as e:
        print(f'{maximize_window} [', end='')
        print(Fore.RED + 'FAILED')
        print(']')
        print(f'{e}')

    try:
        logging_in = 'Logging in'
        companycode = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'userCompany')))
        companycode.send_keys(company_code)
        username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'j_username')))
        username.send_keys(user_name)
        credentials = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'j_password')))
        credentials.send_keys(password)
        credentials.submit()
        time.sleep(1)
        
        print(f'{logging_in} [', end='')
        print(Fore.GREEN + 'SUCCESS', end='')
        print(']')
    except Exception as e:  
        print(f'{logging_in} [', end='')
        print(Fore.GREEN + 'FAILED', end='')
        print(']')
        print(f'{e}')

def trip_tab_nav(driver):
	try:
		trip_tab = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//a[@title="Trips "]')))
		trip_tab.click()
	except Exception as e:
		print(Fore.RED + f'Error when navigating to Trips tab: \n{e}')
	time.sleep(5)


def assigned_trips_page(driver):
    try:
        # Navigate to assigned trips page
        select_status = Select(WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'f_2'))))
        select_status.select_by_value('38')
        WebDriverWait(driver, 20).until(EC.invisibility_of_element((By.ID, 'loading_div')))
        
        # Search button click
        search_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.NAME, 'btnFilter')))
        search_button.click()
        
        #WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.ID, 'loading_div')))
        #WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'completeTrip')))
        
    except Exception as e:
        print(Fore.RED + f'Error when navigating to Assigned Trips page: \n{e}')


#encompasses the assigned function with the addition of querying the previous day
def yesterday_trips(driver):
	try:
		#select 'assigned' from the dropdown
		select_status = Select(WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'f_2'))))
		time.sleep(1)
		select_status.select_by_value('38')
		time.sleep(1)

		date_element = WebDriverWait(driver, 20).until(
               EC.presence_of_element_located((By.XPATH, "//div[@id='f_7_div']//select[@id='drpdownEstimatedDate']"))
               )
		select_date = Select(date_element)
		select_date.select_by_value("-1d")
        # placed here for troubleshooting
		search_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'btnFilter')))
		search_button.click()
		time.sleep(2)
	except Exception as e:
		print(Fore.RED + f'Error occured when navigating to YESTERDAYs trips page: \n{e}')


'''def weekly_trips(driver):
	try:
		#select 'assigned' from the dropdown
		select_status = Select(WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'f_2'))))
		time.sleep(1)
		select_status.select_by_value('38')
		time.sleep(1)

		date_element = WebDriverWait(driver, 20).until(
               EC.presence_of_element_located((By.XPATH, "//div[@id='f_7_div']//select[@id='drpdownEstimatedDate']"))
               )
		select_date = Select(date_element)
		select_date.select_by_value("-1d")
        # placed here for troubleshooting
		search_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'btnFilter')))
		search_button.click()
		time.sleep(2)
	except Exception as e:
		print(Fore.RED + f'Error occured when navigating to YESTERDAYs trips page: \n{e}')
'''

def rider_links(driver):
    user_links = WebDriverWait(driver, 10).until(lambda x: x.find_elements(By.XPATH, '//a[starts-with(@href, "#/trip/tripview/")]'))
    return user_links

def process_rider_tasks_today(driver):
    while True:
        try:
            # Wait for the presence of the elements
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[starts-with(@href, "#/trip/tripview/")]')))
            
            # Retrieve the user links
            user_links = rider_links(driver)
            
            # If no user links are found, break the loop
            if not user_links:
                break
            
            # Process each user link
            for link in user_links:
                try:
                    user_info_propagate(link, driver)
                    assigned_trips_page(driver)
                except StaleElementReferenceException:
                    # Retry the operation if the element is stale
                    user_links = rider_links(driver)
                    user_info_propagate(link, driver)
                    
            
            # Call yesterday_trips after processing each link
            #assigned_trips_page(driver)
            

        except StaleElementReferenceException:
            # Retry the whole loop if the element is stale
            continue

def process_rider_tasks_yesterday(driver):
    while True:
        try:
            # Wait for the presence of the elements
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//a[starts-with(@href, "#/trip/tripview/")]')))
            
            # Retrieve the user links
            user_links = rider_links(driver)
            
            # If no user links are found, break the loop
            if not user_links:
                break
            
            # Process each user link
            for link in user_links:
                try:
                    user_info_propagate(link, driver)
                    yesterday_trips(driver)
                except StaleElementReferenceException:
                    # Retry the operation if the element is stale
                    user_links = rider_links(driver)
                    user_info_propagate(link, driver)
                    
            
            # Call yesterday_trips after processing each link
            #yesterday_trips(driver)
            

        except StaleElementReferenceException:
            # Retry the whole loop if the element is stale
            continue


'''def process_rider_trips_weekly(driver):
    while True:
        try:
            # Wait for the presence of the elements
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//a[starts-with(@href, "#/trip/tripview/")]')))
            
            # Retrieve the user links
            user_links = rider_links(driver)
            
            # If no user links are found, break the loop
            if not user_links:
                break
            
            # Process each user link
            for link in user_links:
                try:
                    user_info_propagate(link, driver)
                    weekly_trips(driver)
                except StaleElementReferenceException:
                    # Retry the operation if the element is stale
                    user_links = rider_links(driver)
                    user_info_propagate(link, driver)

        except StaleElementReferenceException:
            # Retry the whole loop if the element is stale
'''

#encompasses the assigned function with the addition of querying the previous day
#Need to reformat this, extremely unwieldy for troubleshooting but I don't have the time
def user_info_propagate(user_link, driver):
    user_link.click()
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'tripActions')))
    while True:
        try:
            dropdown_menu = driver.find_element(By.ID, 'tripActions')
            dropdown_menu.click()
            break
        except StaleElementReferenceException:
            continue

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'completeTrip')))
    
    while True:
        try:
            select_complete_trip_option = driver.find_element(By.ID, 'completeTrip')
            select_complete_trip_option.click()
            break
        except StaleElementReferenceException:
            continue

    #xpath to riders name to pull variable for riders name
    xpath = '//*[@id="main"]/div/div/nu-trip-details/div/div[1]/div[1]/div/div[1]/span[3]/span[2]'

    # find the element and get its text
    while True:
        try:
            user_name = driver.find_element(By.XPATH, xpath).text
            break
        except StaleElementReferenceException:
            continue

    # get the template path and the file path
    current_dir = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(current_dir, 'signatures', f"rider.png")
    file_path = os.path.join(current_dir, 'signatures', f"{user_name}.png")

    # find the "Select File" button
    while True:
        try:
            select_file_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//span[@class="fileLeft m-0"]')))
            # click the "Select File" button
            select_file_button.click()
            break
        except StaleElementReferenceException:
            continue
        
    time.sleep(1)

    # type the file path and press Enter
    if os.path.exists(file_path):
        time.sleep(.5)
        pyautogui.write(file_path)
        time.sleep(.5)
    else:
        time.sleep(1)
        new_signature = os.path.join(current_dir, 'signatures', f'{user_name}.png')
        shutil.copy2(template_path, new_signature)
        pyperclip.copy(new_signature)
        pyautogui.hotkey('ctrl', 'v')
        #pyautogui.write(new_signature)
    time.sleep(.5)
    pyautogui.press('enter')
    

    input_fields = driver.find_elements(By.XPATH, '//label[text()="Scheduled Date & Time"]/following-sibling::input')

    # Get the value of the first input field
    pick_up_time = input_fields[0].get_attribute('value')
    # Get the value of the second input field
    drop_off_time = input_fields[1].get_attribute('value')

    #convert to 24-hour format
    pick_up_time_24h = datetime.strptime(pick_up_time, '%b %d, %Y %I:%M:%S %p').strftime('%H%M')
    # Convert drop_off_time to 24-hour format
    drop_off_time_24h = datetime.strptime(drop_off_time, '%b %d, %Y %I:%M:%S %p').strftime('%H%M')
    # Input pick_up_time_24h into the fields
    driver.find_element(By.ID, 'puArrivalTime').send_keys(pick_up_time_24h)
    driver.find_element(By.ID, 'actualPickUpTime').send_keys(pick_up_time_24h)
    driver.find_element(By.ID, 'puDepartureTime').send_keys(pick_up_time_24h)
    # Input drop_off_time_24h into the fields
    driver.find_element(By.ID, 'transArrivalTime').send_keys(drop_off_time_24h)
    driver.find_element(By.ID, 'actualTransTime').send_keys(drop_off_time_24h)
    driver.find_element(By.ID, 'transDepartureTime').send_keys(drop_off_time_24h)

    save_button = driver.find_element(By.XPATH, '//button[@class="btn btn-sm btn-primary btn70"]')

    # click the "Save" button
    time.sleep(.25)
    save_button.click()
    # wait for the "Trip" link to appear and handle StaleElementReferenceException
    for _ in range(3):  # Retry up to 3 times
        try:
            trip_link = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, 'Trip')))
            time.sleep(1)
            trip_link.click()
            break  # Exit the loop if successful
        except StaleElementReferenceException:
            time.sleep(1)  # Wait a bit before retrying
        except TimeoutException:
            print("Timeout waiting for 'completeTrip' element.")
        except NoSuchElementException:
            print("Element 'completeTrip' not found.")
