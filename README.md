# User Manual for Check-in Today Okay!

## Signup

Send an email like the one below to checkin-today-okay@gmail.com

Your email tells us us what to do in case you do not check in 
tomorrow.   We will send a copy of your email to the address you specify following "to:".  When testing, 
use one of your own email addresses.

```
to: caregiver@gmail.com

Dear Caregiver, if you are receiving this message it could mean that I need help.  

Could you please check with me?  Thanks, I would really appreciate it.

Your friend,

  Concerned About Being Alone All The Time
```

## Check-in

A reminder will be sent to you at 6 PM.  Hit Reply, Send.  No need to write a message.  You can also send an edited sign-up email again.

## Alert

If you do not send us an email by 9 PM, we send the alert email. 

# What is it?

It is a dedicated gmail account and a python script running on a cron.  The code reads the last two days of 
email sent to checkin-today-okay@gmail.com.  If you sent an email yesterday, but not the today, we follow the 
instructions in yesterday's email.  You prevent the alert by sending the same message, with instructions, every day.

# Three-day Demo in 6 Easy Steps:

1.  send the first email to sign up.  You get a welcome message, sent by the gmail Vacation Responder.

2.  your email counts as both signup and first day checkin.  So nothing happens today.  This is a demo that requires yoda-like patience.

3.  tomorrow at 6 PM you will get a reminder email.  Hit reply and send any time before 9 PM.

4.  notice that at 9 PM there was no alert email generated, because you checked in.  It's working!

5.  the next day at 6 PM you will get another reminder email.  In this part of the test, you are pretending to be in trouble and can't check in.  So DO NOT RESPOND to the reminder email.

6.  the next day at 9 PM you have failed to check in.  The script sends an email alert.    The email goes to the address that comes after "to:" in the body of the email you sent the day before (today).  The body of the email is the same as your original signup email.

If you see the alert email come in, it's working!

At this point, we assume you are dead and you are "removed" from the system.  It has only a 2-day memory and you are about to drop off.  It will not send any more reminders or alerts after this first one.  

To get back in to the system, you can either hit reply to the reminder email, or send the first message again but this time with the real message and the real address you want to send the alert.


In step 3, you can also check in by sending the same email you sent today.  But that requires cut and paste.  Hitting reply is easier.
