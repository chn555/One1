#!/usr/bin/env python2
from bs4 import BeautifulSoup
import requests
import urllib3
import re
import time
from requests.exceptions import ConnectionError
urllib3.disable_warnings()
import nexmo
import sys

USR = "chn566"
PWD = "itwmedbwphqaklsc"


def send_email(user, pwd, recipient, subject, body):
    import smtplib

    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print ('successfully sent the mail')
    except:
        print ("failed to send mail")

def get_call_number():
    global phone_number
    try :
        #get the page and parse it
        r = requests.get("https://62.0.34.68/benefitmobile/cust/one1/frmwo.aspx?tel={}".format(phone_number), verify=False)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
# call number as global, to be used outside this function
        global number

# remove all the text, leave only the numbers
        number = soup.findAll("span", {"id" : "lblTitle"}, text=True)[0].text
        number = re.sub("\D", "", number)

    except IndexError:
        print ("Something went wrong, probably wrong phone number.")
    except ConnectionError:
        print ("System is offline, retrying in 5min")
        time.sleep(300)
        get_call_number()

    return number

file = open("pnum.txt","r")
phone_number = file.read()

file2 = open("email.txt","r")
EMAIL = file2.read()


call = open("callnum.txt","w")
call.write(get_call_number())

send_email(user=USR, pwd=PWD, recipient=EMAIL, subject="One1 Call Notification System",
           body="Notification system started")
