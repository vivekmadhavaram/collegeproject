#this is the project done by me using python and raspberry pi  in which when a button is pressed, a web cam captures a image, sends it to the owner,based on owner’s reply door gets opened




import RPi.GPIO as GPIO
from cv2 import *
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import imaplib
import email

mail = imaplib.IMAP4_SSL('imap.gmail.com')
(retcode, capabilities) = mail.login('bapiraj1998@gmail.com','bapiraj123')

LDR=3
b1=20
b2=21
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LDR,GPIO.IN)
GPIO.setup(b1,GPIO.OUT)
GPIO.setup(b2,GPIO.OUT)
GPIO.output(b2,GPIO.HIGH)
GPIO.output(b1,GPIO.HIGH)

#here mail is being sent

def send_email(iD,bapiraj11):
    print("Sending eMail")
    toaddr = 'bapiraj11@gmail.com'
    fromaddr = 'bapiraj1998@gmail.com'
    toaddrs  = str(iD)
    msg = MIMEMultipart()

    text = MIMEText(str(bapiraj11))
    msg['Subject'] ='Testing'
    msg.attach(text)
    a='test.jpg'      #image
    fp=open(a,'rb')
    img=MIMEImage(fp.read())
    fp.close()
    msg.attach(img)
    # Credentials (if needed)
    username = 'bapiraj1998@gmail.com'
    password = 'bapiraj123'

    # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username,password) #logging into senders account
    server.sendmail(fromaddr, toaddrs, msg.as_string())#sending msg
    server.quit()
    print("eMail Sent SUCCESSFULLY")

#capturing image

def snap():
    print("Your picture is being taken")
    cam=VideoCapture(0)
    s,img=cam.read()
    if s:
        temp="test.jpg"
        imwrite(temp,img)
    cam.release()
    print("Your picture is taken")

#verifying owner’s reply

def mail_check():
 while True:    
        n=0
        mail.list()
        mail.select('inbox')
        (retcode, messages) = mail.search(None, '(UNSEEN)')
        if retcode == 'OK':
            for num in messages[0].split() :
                print 'Processing '
                n=n+1
                typ, data = mail.fetch(num,'(RFC822)')
                for response_part in data:
                    if isinstance(response_part, tuple):
                        original = email.message_from_string(response_part[1])
                        if(original['From']=="Bapi Raj <bapiraj11@gmail.com>"):
                           if(original['Subject']=="unlock"):
                              GPIO.output(b2,GPIO.LOW)
                              GPIO.output(b1,GPIO.LOW)
                              print "The door is unlocked, You may get in"
                              time.sleep(20)
                              GPIO.output(b2,GPIO.HIGH)
                              GPIO.output(b1,GPIO.HIGH)
                              return
                           else:
                              GPIO.output(b2,GPIO.HIGH)
                              GPIO.output(b1,GPIO.HIGH)
                              print "You are not allowed"


print "Please ring the door bell"
while (True):
 if(GPIO.input(LDR)==0):
  continue
 else:
  print "Door bell is rung"
  time.sleep(5)
  snap()
  send_email("bapiraj11@gmail.com","Your door is being knocked Please Respond")
  print "Please wait for the response of the user"
  time.sleep(10)
  mail_check()                            

