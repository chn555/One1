from bs4 import BeautifulSoup
import requests
import urllib3
import re
import time
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
    return number
get_call_number()
number = int(get_call_number())
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
    send_email(user="chn566", pwd="itwmedbwphqaklsc", recipient="chn566work@gmail.com",subject="One1 Call Notification System", body="Notification system started")
    while True :
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

            send_email(user="chn566", pwd="itwmedbwphqaklsc", recipient="chn566work@gmail.com",
                       subject="One1 Call Notification System", body=msg)
            number = updated_calls
        elif number > updated_calls:
            diff = int(number) - int(updated_calls)
            msg = "{} call(s) removed, {} calls total.".format(diff, updated_calls)

            send_email(user="chn566", pwd="itwmedbwphqaklsc", recipient="chn566work@gmail.com",
                       subject="One1 Call Notification System", body= msg)
            number = updated_calls
        print msg
        time.sleep(60)

call_checker()

#send_email(user = "chn566",pwd= "itwmedbwphqaklsc",recipient= "chn566work@gmail.com",subject= "One1 Call Notification System",body= "Current number of calls is {}".format(number))
print number

