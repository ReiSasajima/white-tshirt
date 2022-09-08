import chromedriver_binary # <- これでChromeDriverをPATHに自動追加してくれる
from selenium import webdriver

driver = webdriver.Chrome()
driver.get('https://google.com')