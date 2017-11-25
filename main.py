from bs4 import BeautifulSoup
import requests
import urllib3
import re
urllib3.disable_warnings()

def get_call_number():

# get the page and parse it
    r = requests.get("https://62.0.34.68/benefitmobile/cust/one1/frmwo.aspx?tel=0524098844", verify=False)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")

# call number as global, to be used outside this function
    global number

# remove all the text, leave only the numbers
    number = soup.findAll("span", {"id" : "lblTitle"}, text=True)[0].text
    number = re.sub("\D", "", number)

get_call_number()
print number

