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

key = open("key.txt","r")
secret = open("secret.txt","r")
KEY = key.read()
SECRET = secret.read()
client = nexmo.Client(key=KEY, secret=SECRET)


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



call = open("callnum.txt","w")
call.write(get_call_number())


client.send_message({
    'from': 'One1',
    'to': "972"+str(phone_number),
    'text': "Notification system started",
})
