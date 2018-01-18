from bs4 import BeautifulSoup
import requests
import urllib3
import re
import time
import datetime
from requests.exceptions import ConnectionError
urllib3.disable_warnings()
import nexmo
client = nexmo.Client(key="2c70516f", secret="0a7a75d30074b55f")

file = open("pnum.txt","r")
text = open("callnum.txt","r")

phone_number = int(file.read())
old_call_number = int(text.read())
global global_phone_number
global_phone_number = "972"+str(phone_number)
print global_phone_number


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
        # get the page and parse it
        r = requests.get("https://62.0.34.68/benefitmobile/cust/one1/frmwo.aspx?tel=0{}".format(phone_number),
                         verify=False)
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        # call number as global, to be used outside this function

        number = 0
        global number
        # remove all the text, leave only the numbers
        number = soup.findAll("span", {"id" : "lblTitle"}, text=True)[0].text
        print number
        number = re.sub("\D", "", number)
        print number

    except IndexError:
        print ("Something went wrong, probably wrong phone number.")
    except ConnectionError:
        print ("System is offline, retrying in 5min")
        time.sleep(300)
        get_call_number()


    return number

def compare_calls () :

    global msg
    msg = "test msg"
    if current_call_number == old_call_number:
       pass
    elif current_call_number > old_call_number:
        diff = int(current_call_number) - int(old_call_number)
        msg = "{} call(s) added, {} calls total.\n"\
              "{:%H:%M}".format(diff, current_call_number, datetime.datetime.now())
        send_SMS(global_phone_number, msg)
        print msg

    elif old_call_number > current_call_number:
        diff = int(old_call_number) - int(current_call_number)
        msg = "{} call(s) removed, {} calls total.\n" \
              "{:%H:%M}".format(diff, current_call_number, datetime.datetime.now())
        send_SMS(global_phone_number, msg)
        print msg

def compare_calls_email () :

    global msg
    msg = "test msg"
    if current_call_number == old_call_number:
       pass
    elif current_call_number > old_call_number:
        diff = int(current_call_number) - int(old_call_number)
        msg = "{} call(s) added, {} calls total.\n"\
              "{:%H:%M}".format(diff, current_call_number, datetime.datetime.now())
        send_email(user="chn566", pwd="itwmedbwphqaklsc", recipient="chn566work@gmail.com",
               subject="One1 Call Notification System", body=msg)
        print msg

    elif old_call_number > current_call_number:
        diff = int(old_call_number) - int(current_call_number)
        msg = "{} call(s) removed, {} calls total.\n" \
              "{:%H:%M}".format(diff, current_call_number, datetime.datetime.now())
        send_email(user="chn566", pwd="itwmedbwphqaklsc", recipient="chn566work@gmail.com",
                   subject="One1 Call Notification System", body=msg)
        print msg

def send_SMS(x,y):
    client.send_message({
        'from': 'One1',
        'to': x,
        'text': y,
    })

current_call_number = int(get_call_number())


compare_calls()

text.close()







text = open("callnum.txt","w")
text.write(str(current_call_number))
file.close()
text.close()