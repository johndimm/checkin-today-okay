import smtplib
import time
import imaplib
import email
from datetime import timedelta, date, datetime, time
from dateutil.parser import parse
import smtplib, ssl
import re
import sys
import html2text
import os

import io

def main():

    SENDER_EMAIL  = "Check-in Today Okay! <checkintodayokay@gmail.com>"
    FROM_EMAIL    = "checkintodayokay@gmail.com"
    FROM_PWD      =  os.environ.get('password')

    print ("FROM_PWD:", FROM_PWD)
    dateFormat = "%d-%b-%Y"

    def getFilter():
        #
        #  day1 is yesterday, day 2 is today 
        #
        today = date.today() + timedelta(days=0)
        day1 = today - timedelta(days=1)
        day2 = today - timedelta(days=0)

        d1 = day1.strftime(dateFormat)
        return (day1, day2, '(SINCE "%s")' % d1)

    def login():
        SMTP_SERVER = "imap.gmail.com"
        # SMTP_PORT   = 993
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL,FROM_PWD)
        mail.select('inbox')
        return mail

    def clean(msg):
        #regex = "<[^>]*>"
        #s1 = re.sub(regex, "", html)
        ctype = msg.get_content_type()
        pay = msg.get_payload()
        if ctype == 'text/plain':
            return pay

        s1 = html2text.html2text(pay)
        s2 = re.sub(" *= *", " ", s1)
        s3 = re.sub("\n\n", "\n", s2)
        #ßre.sub("&nbsp;", " ", s2)
        return s3

    def getEmailContents(msg):
        contents = ''
        if msg.is_multipart():
           for payload in msg.get_payload():
           # if payload.is_multipart(): ...
               contents += clean(payload)
        else:
            contents += clean(msg)

       # parts = []
       # for part in msg.walk():
            #if part.get_content_type() == 'text/plain':
       #         parts.append( part.get_payload() )
       # contents = ''.join(parts)

        # Remove email quoting.
        print ("contents before =====\n%s\n=========== " % contents)

        #
        # Extract the quoted email in this email.
        # Contents is the whole enail if it's not a reply.
        #
        quotedLines = re.findall(r"^>.*", contents, re.MULTILINE)
        if len(quotedLines) > 0:
            a = []
            for line in quotedLines:
                cleaned = re.sub(r" ?^>? {0,2}", '', line, re.MULTILINE)
                print ("cleaned:", cleaned)
                a.append(cleaned)
            contents = "\n".join(a)
            contents = contents.strip()

        print ("contents after =====\n%s\n=========== " % contents)

        return contents

    def getMessages(filter):
        messages = []

        typ, data = mail.search(None, filter )
        if len(data) == 0:
            return

        mail_ids = data[0]
        id_list = mail_ids.split()   
        print ('ids:', id_list)

        ask = '(RFC822)'
        for i in id_list:
 
            typ2, data2 = mail.fetch(i, ask )
            rawEmail = data2[0][1]
            #msg = email.message_from_string(rawEmail)    # python 2.7
            msg = email.message_from_bytes(rawEmail)      # python 3

            efrom = msg['From']
            edate = parse(msg['date']).date()
            econtents = getEmailContents(msg) 

            message = {'from': efrom, 'date': edate, 'contents': econtents}
            messages.append(message)         

        return messages


    def splitMessages(messages, day1, day2):
        day1Messages = dict()
        day2Messages = dict()
        for m in messages:
            efrom = m['from']
            if m['date'] == day1:
                day1Messages[efrom] = m['contents']
            if m['date'] == day2:
                day2Messages[efrom] = ''
        return (day1Messages, day2Messages)        

    def findExceptions(day1Messages, day2Messages):        
        # 
        # Find senders on day 1 that did not send on day2.
        #
        alerts = []
        
        #for sender, message in day1Messages.iteritems():    #python 2.7
        for sender, message in day1Messages.items():         #python 3
            if not (sender in day2Messages):
                alerts.append({"from": sender, "contents": message})

        return alerts

    def nowTime():
        now = datetime.now()
        return "%s:%s %s:%s:%s" % (now.month, now.day, now.hour, now.minute, now.second)

    def sendReminders(day1Messages):
        for sender, message in day1Messages.items():
            sendMessage(sender, message, 'Check-in Today Okay? by 9 pm (%s)' % nowTime())

    def sendAlert(alert):
        contents = alert['contents']
        sender = alert['from']
        receiver = ''

        regex = re.compile(r"to:(.*)", re.MULTILINE)
        matches = regex.search(contents)
        if matches:
            receiver = matches.group(1).strip()

        sendMessage(receiver, contents, 'Check-in Today NOT Okay! %s (%s)' % (sender, nowTime()))

    def sendMessage(receiver, contents, subject):
        print ("sending message: %s, %s %s" % (receiver, subject, contents))

        PORT = 465  # For SSL
        SMTP_SERVER = "smtp.gmail.com"
        
        message = """From:%s
Subject: %s

%s
""" % (SENDER_EMAIL, subject, contents)

        print ("receiver: %s, message:\n=====\n %s \n=======\n" % (receiver, message))

        server = smtplib.SMTP_SSL(SMTP_SERVER, PORT)
        server.login(FROM_EMAIL, FROM_PWD)
        server.sendmail(FROM_EMAIL, receiver, message)    
#
# Read email, send reminders, send alerts.
#
    try:
        mail = login()
        (day1, day2, filterDef) = getFilter()
        messages = getMessages(filterDef)
        (day1Messages, day2Messages) = splitMessages(messages, day1, day2)

        action = 'alert'
        if len(sys.argv) > 1:
            action = sys.argv[1]

        if action == 'reminder':
            sendReminders(day1Messages)

        elif action == 'alert':
            alerts = findExceptions(day1Messages, day2Messages)    
            for alert in alerts:
                sendAlert(alert)

    except:
       print("Error:", sys.exc_info()[0])

main()
