# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

def send_email(message="", subject="EReport of Twitter Bot"):
    msg = MIMEText(message)

    msg['Subject'] = subject

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    try:
        s = smtplib.SMTP('localhost')
        s.sendmail('root@rent-history.com', 'r.vooda@gmail.com', msg.as_string())
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
