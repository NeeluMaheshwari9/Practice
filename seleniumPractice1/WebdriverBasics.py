import time
from selenium import webdriver
driver = webdriver.Chrome(executable_path="C:\Drivers\chromedriver_win32 (1)\chromedriver.exe")
driver.get("http://www.google.com")
print(driver.title)
print(driver.current_url)
driver.get("https://www.youtube.com/watch?v=FRn5J31eAMw")
print(driver.title)
print(driver.current_url)
time.sleep(5)
driver.back()
driver.maximize_window()
time.sleep(5)
driver.forward()
# driver.close()
# To exit chrome
driver.quit()