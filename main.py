from bs4 import BeautifulSoup
import requests
import urllib3
import re
import time
from requests.exceptions import ConnectionError
urllib3.disable_warnings()

def get_phone_number():
    global phone_number
    phone_number = raw_input("Enter phone number : ")

    if phone_number == "1" :
        phone_number = "0524098844"
    elif len(phone_number) != 10:
        print "Invalid phone number, try again. "
        get_phone_number()
    else:
        pass

    return str(phone_number)

def get_email():
    global Email
    Email = raw_input("Enter e-mail address : ")
    return Email

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
        print "Something went wrong, probably wrong phone number."
    except ConnectionError:
        print "System is offline, retrying in 5min"
        time.sleep(300)
        get_call_number()

    return number
# copied from stackoverflow
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
        print 'successfully sent the mail'
    except:
        print "failed to send mail"

msg = "nothing"
def call_checker():
    global Email
    send_email(user="chn566", pwd="itwmedbwphqaklsc", recipient=Email, subject="One1 Call Notification System", body="Notification system started")
    while True :
        #calls number
        global number
        print number
        updated_calls = get_call_number()
        print updated_calls
        global msg
        if updated_calls == number:
            pass
        elif updated_calls > number:
            diff = int(updated_calls) - int (number)
            msg = "{} call(s) added, {} calls total.".format(diff, updated_calls)

            send_email(user="chn566", pwd="itwmedbwphqaklsc", recipient=Email,
                       subject="One1 Call Notification System", body=msg)
            number = updated_calls
        elif number > updated_calls:
            diff = int(number) - int(updated_calls)
            msg = "{} call(s) removed, {} calls total.".format(diff, updated_calls)

            send_email(user="chn566", pwd="itwmedbwphqaklsc", recipient=Email,
                       subject="One1 Call Notification System", body= msg)
            number = updated_calls
        print msg
        time.sleep(60)


phone_number = get_phone_number()
Email = str(get_email())
get_call_number()
number = int(get_call_number())
call_checker()

#send_email(user = "chn566",pwd= "itwmedbwphqaklsc",recipient= "chn566work@gmail.com",subject= "One1 Call Notification System",body= "Current number of calls is {}".format(number))
print number

