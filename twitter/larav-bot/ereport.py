# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

def send_email(message="", subject="EReport of Twitter Bot"):
    msg = MIMEText(message)

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = subject
    msg['From'] = 'r.vooda@gmail.com'
    msg['To'] = 'rvooda@freewheel.tv'

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    try:
        s = smtplib.SMTP('smtp.gmail.com',587)
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login('ravi@mafianz.com', 'mafiandeath')
        s.sendmail('r.vooda@gmail.com', 'rvooda@freewheel.tv', msg.as_string())
        s.quit()
        return True
    except Exception as e:
        print e
        return False

if __name__ == "__main__":
    if send_email(message="Hello Ravi!"):
        print "Successfully sent the mail"
    else:
        print "Sorry"
