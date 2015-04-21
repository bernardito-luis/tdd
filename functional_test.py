from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8008')

assert 'Django' in browser.title
