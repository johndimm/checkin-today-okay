import smtplib
import time
import imaplib
import email
from datetime import timedelta, date, datetime, time, tzinfo
from dateutil.parser import parse
import smtplib, ssl
import re
import sys
import html2text
import os

from pytz import timezone
import tzlocal

import quotequail

#import io

def main():

    SENDER_EMAIL  = "Check-in Today Okay! <checkintodayokay@gmail.com>"
    FROM_EMAIL    = "checkintodayokay@gmail.com"
    FROM_PWD      =  os.environ.get('password')

    DATE_FORMAT   = "%d-%b-%Y"
    SEND_ALERT_TO = 'send alert to:'
    DATE_OFFSET   = 0
    DO_SEND       = True

    def local_date(utc_time):
            return utc_time.astimezone(tzlocal.get_localzone()).date()

    def getFilter():
        #
        #  day1 is yesterday, day 2 is today 
        #
        today = date.today() + timedelta(days=DATE_OFFSET)
        day1 = today - timedelta(days=1)
        day2 = today - timedelta(days=0)

        d1 = day1.strftime(DATE_FORMAT)
        print ("d1:%s, day1:%s, day2:%s" % (d1, day1 ,day2))
        return (day1, day2, '(SINCE "%s")' % d1)

    def login():
        SMTP_SERVER = "imap.gmail.com"
        # SMTP_PORT   = 993
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')
        return mail

    def clean(msg, mime):
        ctype = msg.get_content_type()
        #print('type:' + ctype)
        p = msg.get_payload(decode=True)
        pay = p.decode()

        m = ''
        if mime == 'text/plain' and ctype == mime:
           m = pay

        if mime == 'text/html' and ctype == mime:
            m = html2text.html2text(pay)

        return m

    def getEmailContents(msg):
        plain = ''
        html = ''
        if msg.is_multipart():
           for payload in msg.get_payload():
               plain += clean(payload, 'text/plain')
               html += clean(payload, 'text/html')

        else:
            plain += clean(msg, 'text/plain')
            html += clean(msg, 'text/html')

        contents = ''
        if len(html) > 0:
            contents = html
        else:
            contents = plain    

        #print ("contents original: ", contents)

        quoted = quotequail.quote(contents)
        for line in quoted:
            if not line[0]:
                contents = line[1]
                break
            else:
                contents = line[1]

        # print ("contents before: ", contents)

        contents = re.sub("^( *> *)*", "", contents, flags=re.M) 
        contents = re.sub("\n\n", "\n", contents, re.MULTILINE)
        contents = re.sub("\s+$", "", contents, re.MULTILINE | re.DOTALL)
        contents = re.sub("^\s+", "", contents, re.MULTILINE | re.DOTALL)

        receiver = ''
        regex = re.compile(r"%s[\s\W]*([^\s\)\]]*)[\s\]]*" % SEND_ALERT_TO, re.MULTILINE | re.DOTALL)
        matches = regex.search(contents)
        if matches:
            receiver = matches.group(1).strip()
            contents = re.sub(regex, '', contents)
            contents = re.sub(r"\(mailto:[^\)]*[\)\]]*", '', contents)

        # print ("contents after: ", contents)
        print ("receiver: ", receiver)

        return (receiver, contents)

    def getMessages(filter):
        messages = []

        typ, data = mail.search(None, filter )
        if len(data) == 0:
            return

        mail_ids = data[0]
        id_list = mail_ids.split()   
        #print ('ids:', id_list)

        ask = '(RFC822)'
        for i in id_list:
 
            typ2, data2 = mail.fetch(i, ask )
            rawEmail = data2[0][1]
            #msg = email.message_from_string(rawEmail)    # python 2.7
            msg = email.message_from_bytes(rawEmail)      # python 3
            #print ("getMessages: \n=====%s======\n", msg.keys())

            efrom = msg['From']
            _date = msg['date']

            utc_time = parse(_date)
            edate = local_date(utc_time)

            (receiver, econtents) = getEmailContents(msg) 

            message = {'from': efrom, 'receiver': receiver, 'date': edate, 'contents': econtents}
            #print ("message:", message)
            messages.append(message)         

        return messages


    def splitMessages(messages, day1, day2):
        day1Messages = dict()
        day2Messages = dict()

        for m in messages:
            efrom = m['from']
            if m['date'] == day1:
                day1Messages[efrom] = m
            if m['date'] == day2:
                day2Messages[efrom] = null
        print ("day1: %s, day2: %s" % (
            len(day1Messages), 
            len(day2Messages)
        ))        
        return (day1Messages, day2Messages)        

    def findExceptions(day1Messages, day2Messages):        
        # 
        # Find senders on day 1 that did not send on day2.
        #
        alerts = []
        
        #for sender, message in day1Messages.iteritems():    #python 2.7
        for sender, m in day1Messages.items():         #python 3
            if not (sender in day2Messages):
                alerts.append({"from": sender, "receiver": m['receiver'], "contents": m['contents']})

        return alerts

    def nowTime():
        now = datetime.now()
        return "%s:%s %s:%s:%s" % (now.month, now.day, now.hour, now.minute, now.second)

    def sendReminders(day1Messages):
        for sender, m in day1Messages.items():
            body = "send alert to: %s\n\n%s" % (m['receiver'], m['contents'])
            

            sendMessage(sender, body, 'Reminder to Check-in Today Okay (%s)' % nowTime())

    def sendAlert(alert):
        contents = alert['contents']
        sender = alert['from']
        receiver = alert['receiver']

        body = "%s %s\n\n%s" % (SEND_ALERT_TO, receiver, contents)

        sendMessage(receiver, body, 'ALERT! from Check-in Today Okay about %s (%s)' % (sender, nowTime()))

    def sendMessage(receiver, contents, subject):
        print ("%s %s, subject: %s" % (SEND_ALERT_TO, receiver, subject))

        PORT = 465  # For SSL
        SMTP_SERVER = "smtp.gmail.com"
        
        message = """From:%s
Subject: %s

%s
""" % (SENDER_EMAIL, subject, contents)

        #print (message)
        #return 

        if DO_SEND:
            server = smtplib.SMTP_SSL(SMTP_SERVER, PORT)
            server.login(FROM_EMAIL, FROM_PWD)
            server.sendmail(FROM_EMAIL, receiver, message.encode("utf8"))    
        else:
            print ("message: ", message)
#
# Read email, send reminders, send alerts.
#
    try:
        print ("\n=========\n%s" % datetime.now())
        mail = login()
        (day1, day2, filterDef) = getFilter()
        messages = getMessages(filterDef)
        (day1Messages, day2Messages) = splitMessages(messages, day1, day2)

        action = 'alert'
        if len(sys.argv) > 1:
            action = sys.argv[1]

        if action == 'reminder':
            print ("checking for reminders")
            sendReminders(day1Messages)

        elif action == 'alert':
            print ("checking for alerts")
            alerts = findExceptions(day1Messages, day2Messages)    
            for alert in alerts:
                sendAlert(alert)

    except:
       print("Error:", sys.exc_info()[0])

main()
