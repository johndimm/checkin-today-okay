# User Manual for Check-in Today Okay!

This is a free daily check-in program.  You check in every day, and if you can't, we alert your designated caregiver.

## Sign up

Send an email like the one below to checkintodayokay@gmail.com

Your email tells us us what to do in case you do not check in 
tomorrow.   We will send a copy of it to the address you specify following "send alert to:". 

```
send alert to: caregiver@gmail.com

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
email sent to checkintodayokay@gmail.com.  If you sent an email yesterday, but not the today, we follow the 
instructions in yesterday's email.  You prevent the alert by sending the same message, with instructions, every day.

# What is it not?

It's not a web app or a mobile app.  There is no front end. There is no User Interface.  There is no database.  The memory is the inbox of the email account, and only the last two days of that.  There are no accounts.

# Three-day Demo in 6 Easy Steps:

1.  send the first email to sign up.   When testing, use your own address as caregiver.  You get a welcome message, sent by the gmail Vacation Responder.

2.  your email counts as both signup and first day checkin.  So nothing happens today.  This is a demo that requires yoda-like patience.

3.  tomorrow at 6 PM you will get a reminder email.  Hit reply and send any time before 9 PM.

4.  notice that at 9 PM there was no alert email generated, because you checked in.  It's working!

5.  the next day at 6 PM you will get another reminder email.  In this part of the test, you are pretending to be in trouble and can't check in.  So DO NOT RESPOND to the reminder email.

6.  the next day at 9 PM you have failed to check in.  The script sends an email alert.    The email goes to the address that comes after "send alert to:" in the body of the email you sent the day before (today).  The body of the email is the same as your original signup email.

If you see the alert email come in, it's working!

At this point you are no longer in the system.  It has only a 2-day memory and you just dropped off.  It will not send any more reminders or alerts after this first one.  

To get back in to the system, you can either hit reply to the reminder email, or send the first message again but this time with the real message and the real address of your caregiver, the person you want to receive the alert.

In step 3, you can also check in by sending the same email you sent today.  But that requires cut and paste.  Hitting reply is easier.

# Applications

* you live alone and are worried that you could go days without anyone checking on you

* you live alone and coronavirus

* you have incriminating evidence against the mob boss whose henchmen are getting closer and closer.  You put the evidence into an email to checkintodayokay, with the attorney general as caregiver, then send a message to the mob boss explaining all this.  He tells the henchmen to be gentle with you.


