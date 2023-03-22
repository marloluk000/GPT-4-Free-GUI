import pyperclip
import requests
import random
import string
import time
import sys
import re
import os
from selenium import webdriver     
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import poe
import streamlit as st
import os, sys


@st.experimental_singleton
def installff():
  os.system('sbase install geckodriver')
  os.system('ln -s /home/appuser/venv/lib/python3.7/site-packages/seleniumbase/drivers/geckodriver /home/appuser/venv/bin/geckodriver')
_ = installff()
message = ""
trace = True
options=Options()
# profile_path = r"C:\Users\vaibhavarduino\AppData\Roaming\Mozilla\Firefox\Profiles\mpzn1317.default-release-1655467558772"
# options.add_argument("-profile")
# options.add_argument(profile_path)
# options.add_argument("--headless")
trace = True
@st.cache_resource
def get_browser():
    global browser
    options.add_argument("--headless")
    browser = webdriver.Firefox(options=options)
    return browser

def login(email):
    browser.get('https://poe.com/login')
    wait.until(EC.visibility_of_element_located(("xpath", "/html/body/div[1]/main/div/button[2]/div"))).get_attribute("value")

    browser.find_element("xpath","/html/body/div[1]/main/div/button[2]/div").click()
    textbox = browser.find_element("xpath","/html/body/div[1]/main/div/div[2]/form/input")
    textbox.send_keys(email)
    browser.find_element("xpath","/html/body/div[1]/main/div/button[1]").click()

def authorise(otp):
    auth = browser.find_element("xpath","/html/body/div[1]/main/div/div[3]/form/input")
    auth.send_keys(otp)
    auth = browser.find_element("xpath","/html/body/div[1]/main/div/button[2]").click()

def ask(text):
    textbox = browser.find_element("xpath","/html/body/div[1]/div[1]/section/footer/div/div[2]/textarea")
    textbox.send_keys(text)
    browser.find_element("xpath","/html/body/div[1]/div[1]/section/footer/div/div[3]/button").click()
    time.sleep(0.8)
    while True:
        if "Like" in (browser.find_element("xpath","/html/body/div[1]/div[1]/section/div[1]").text):
            break
    data = browser.find_element("xpath","/html/body/div[1]/div[1]/section/div[1]").text
    print(data)
    data = data.split(text)[1]
    data = data.split("Like")[0]    
    return data

def ask2(text):
    browser.get('https://poe.com/gpt-4')
    time.sleep(0.8)
    textbox = browser.find_element("xpath","/html/body/div[1]/div[1]/section/footer/div/div[2]/textarea")
    textbox.send_keys(text)
    browser.find_element("xpath","/html/body/div[1]/div[1]/section/footer/div/div[3]/button").click()
    time.sleep(0.8)
    while True:
        if "Like" in (browser.find_element("xpath","/html/body/div[1]/div[1]/section/div[1]").text) and "Share"  in (browser.find_element("xpath","/html/body/div[1]/div[1]/section/div[1]").text) and "Dislike"  in (browser.find_element("xpath","/html/body/div[1]/div[1]/section/div[1]").text):
            break
    data = browser.find_element("xpath","/html/body/div[1]/div[1]/section/div[1]/div/div[2]/div[1]").text
    data2 = browser.find_element("xpath",'//*[@id="__next"]/div/section/div/div/div[2]/div/div[2]/div/div').text
    if data == data2:
        print("DOne!")
    return data2

API = 'https://www.1secmail.com/api/v1/'
domainList = ['1secmail.com', '1secmail.net', '1secmail.org']
domain = domainList[1]

def banner():
    print(r'''
                         ''~``
                        ( o o )
+------------------.oooO--(_)--Oooo.------------------+
|                                                     |
|                    Mail Swipe                       |
|               [by Sameera Madushan]                 |
|                                                     |
|                    .oooO                            |
|                    (   )   Oooo.                    |
+---------------------\ (----(   )--------------------+
                       \_)    ) /
                             (_/
    ''')

def generateUserName():
    name = string.ascii_lowercase + string.digits
    username = ''.join(random.choice(name) for i in range(10))
    username = username + str(random.randint(1,999))
    return username

def extract():
    getUserName = re.search(r'login=(.*)&',newMail).group(1)
    getDomain = re.search(r'domain=(.*)', newMail).group(1)
    return [getUserName, getDomain]

# Got this from https://stackoverflow.com/a/43952192/13276219
def print_statusline(msg: str):
    last_msg_length = len(print_statusline.last_msg) if hasattr(print_statusline, 'last_msg') else 0
    print(' ' * last_msg_length, end='\r')
    print(msg, end='\r')
    sys.stdout.flush()
    print_statusline.last_msg = msg

def deleteMail():
    global trace
    url = 'https://www.1secmail.com/mailbox'
    data = {
        'action': 'deleteMailbox',
        'login': f'{extract()[0]}',
        'domain': f'{extract()[1]}'
    }
    if trace:

        print_statusline("Disposing your email address - " + mail + '\n')
    req = requests.post(url, data=data)

def checkMails():
    reqLink = f'{API}?action=getMessages&login={extract()[0]}&domain={extract()[1]}'
    req = requests.get(reqLink).json()
    length = len(req)
    if length == 0:
        return None,None,None
    else:
        idList = []
        for i in req:
            for k,v in i.items():
                if k == 'id':
                    mailId = v
                    idList.append(mailId)

        x = 'mails' if length > 1 else 'mail'
        if trace:
            print_statusline(f"You received {length} {x} {mailId}. (Mailbox is refreshed automatically every 5 seconds.)")

        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, r'All Mails')
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)

        for i in idList:
            msgRead = f'{API}?action=readMessage&login={extract()[0]}&domain={extract()[1]}&id={i}'
            req = requests.get(msgRead).json()
            for k,v in req.items():
                if k == 'from':
                    sender = v
                if k == 'subject':
                    subject = v
                if k == 'date':
                    date = v
                if k == 'textBody':
                    content = v
                if k == "htmlBody":
                    attach = v
                    import re

                    # Regular expression to find the verification code
                    try:
                        code = re.findall(r'(?<!#)\b\d{6}\b', attach)[0]
                    except:
                        code = None

            mail_file_path = os.path.join(final_directory, f'{i}.txt')
        

            with open(mail_file_path,'w') as file:
                file.write("Sender: " + sender + '\n' + "To: " + mail + '\n' + "Subject: " + subject + '\n' + "Date: " + date + '\n' + "Content: " + content + '\n'+  str(attach) + '\n')

            return  subject,content,code

# banner()
userInput1 = "N"
ress = st.markdown("Starting...")
newMail = ""
mail = ""
wait = ""
@st.cache_resource(show_spinner=False)
def init():
    with st.spinner("Generating ID"):
        global newMail
        global mail
        global wait
        global browser
        wait =  WebDriverWait(browser, 8)
        newMail = f"{API}?login={generateUserName()}&domain={domain}"
        reqMail = requests.get(newMail)
        mail = f"{extract()[0]}@{extract()[1]}"
    with st.spinner("Logging into GPT-4"):
        login(mail)
    timed = time.time()
    while True:
        with st.spinner("Authorising.."):
            sub,content,code = checkMails()
            if code != None:
                if trace:
                    print(f"Code is {code}")
                authorise(code)
                with st.spinner("Downloading Data.."):
                    client = poe.Client(browser.get_cookie('p-b')['value'])
                return client
            else:
                if time.time() - timed > 30:
                    return None
browser =  get_browser()
client = init() 
if client != None:
        message = st.text_input("How can GPT-4 Help You today?")
        if st.button("ask"):
            old = st.markdown("🔃")
            oddy = ""
            for chunk in client.send_message("beaver", message):
                oddy = oddy  + chunk["text_new"]
                old.write(oddy)
            oddy = ""
            browser.delete_all_cookies()
            init.clear()
# while True:
#     try:
#         if userInput1 == 'N':

#                 newMail = f"{API}?login={generateUserName()}&domain={domain}"
#                 reqMail = requests.get(newMail)
#                 mail = f"{extract()[0]}@{extract()[1]}"
#                 pyperclip.copy(mail)
#                 ress.write("Logging In")
#                 login(mail)
#                 timed = time.time()
                
#                 while True:
#                     sub,content,code = checkMails()
#                     if code != None:
#                         if trace:
#                             print(f"Code is {code}")
#                         ress.write("Authorising..")

#                         authorise(code)
#                         client = poe.Client(browser.get_cookie('p-b')['value'])
#                         message = st.text_input("How can GPT-4 Help You today?")
#                         if st.button("ask"):
#                             oddy = ""
#                             for chunk in client.send_message("beaver", message):
#                                 oddy = oddy  + chunk["text_new"]
#                                 ress.write(oddy)
#                             oddy = ""
#                         browser.delete_all_cookies()
#                         deleteMail()
#                         break
#                     else:
#                         if time.time() - timed > 30:
#                             break

#     except Exception as e:
#         deleteMail()
#         if trace:
#             print(e)
#         if "KeyboardInterrupt" in str(e):
#             break
#         browser.delete_all_cookies()


        # newMail = f"{API}?login={generateUserName()}&domain={domain}"
        # reqMail = requests.get(newMail)
        # mail = f"{extract()[0]}@{extract()[1]}"
        # pyperclip.copy(mail)
        # print("\nYour temporary email is " + mail + " (Email address copied to clipboard.)" + "\n")
        # print(f"---------------------------- | Inbox of {mail} | ----------------------------\n")
        # while True:
        #     checkMails()
        #     time.sleep(5)
# client = poe.Client("QcKrNtoJiMjNzYrc9Hb-YA==")
# message = "What is the meaning of life?."
# for chunk in client.send_message("beaver", message):
#   print(chunk["text_new"], end="", flush=True)






