# wellryde-trip-automation
Automated program for Modivcare NEMT providers.

Requires the following modules:

1. selenium
2. webdriver_manager
3. Colorama
4. Pyautogui


<b>Purpose</b>
This program allows you to connect to the Logisticare web platform and automate rider pickup, will call and drop off times and uploads a signature file. If the rider is new, a new file is created from the 'rider.png' template with the new riders name.

t.py focuses on today's date.
y.py focuses on yesterday's date (today - 1 day)
7day.py is a work in progress to do the last 7 days in the event that new trips were added/missed.
