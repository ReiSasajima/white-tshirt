from selenium import webdriver
from selenium.webdriver.common.keys import Keys as keys

driver = webdriver.Chrome(executable_path="C:\scrapping\chromedriver.exe")
driver.get('https://google.com')