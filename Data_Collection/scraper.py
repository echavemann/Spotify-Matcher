import email
import selenium
from splinter import Browser
import time
Username = ''
Password = ''
Name = ''
Email = ''
browser = Browser()

browser.visit("https://accounts.spotify.com/en/login")
un = browser.find_by_id('login-username')
un.fill(Username)
pw = browser.find_by_id('login-password')
pw.fill(Password)
browser.find_by_id('login-button').click()
time.sleep(1)
url = "https://developer.spotify.com/dashboard/applications/941531055a584ec5ac5a863f4abe730b"
browser.visit(url)
#Click login
browser.find_by_xpath('/html/body/div[1]/div/div/main/section/div[2]/div[2]/div/p[2]/button').click()
#Open Matcher
browser.find_by_xpath('/html/body/div[1]/div/div/main/section/div[3]/div[2]/ul/li[1]/a/div[1]').click()
#Users
time.sleep(0.1)
browser.find_by_xpath('/html/body/div[1]/div/div/main/div/div/section[1]/div[3]/div[2]/div[1]/button[2]').click()
time.sleep(0.1)
#Scroll Down
browser.execute_script("window.scrollTo(400, document.body.scrollHeight);")
#Click Add
browser.find_by_xpath('/html/body/div[1]/div/div/main/div/div/section[2]/section/div/div[3]/div/a/i').click()
#Input
browser.find_by_xpath('/html/body/div[1]/div/div/main/div/div/section[2]/section/div/div[4]/div/div/div/div/div[2]/div/div[1]/label/input').fill(Name)
browser.find_by_xpath('/html/body/div[1]/div/div/main/div/div/section[2]/section/div/div[4]/div/div/div/div/div[2]/div/div[2]/label/input').fill(Email)
#CLick add
browser.find_by_xpath('/html/body/div[1]/div/div/main/div/div/section[2]/section/div/div[4]/div/div/div/div/div[3]/div/button[1]').click()
