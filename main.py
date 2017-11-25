from bs4 import BeautifulSoup
import requests
import urllib3
import re
urllib3.disable_warnings()


r = requests.get("https://62.0.34.68/benefitmobile/cust/one1/frmwo.aspx?tel=0524098844", verify=False)
data = r.text
soup = BeautifulSoup(data, "html.parser")

number = soup.findAll("span", {"id" : "lblTitle"}, text=True)[0].text
number = re.sub("\D", "", number)


print number

