# import necessary packages
 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


class EmailUpdate:
# create message object instance
    
    def send_email_update(self):
        
        # setup the parameters of the message
        password = "Giltby3!"
        self.msg['From'] = "thatdambot@gmail.com"
        self.msg['To'] = 'kstrecker@gilt.com'
        self.msg['Subject'] = "An update from That Dam Bot"
        
        # add in the message body
        self.msg.attach(MIMEText(self.message, 'plain'))
        
        #create server
        server = smtplib.SMTP('smtp.gmail.com: 587')
        
        server.starttls()
        
        # Login Credentials for sending the mail
        server.login(self.msg['From'], password)
        
        
        # send the message via the server.
        server.sendmail(self.msg['From'], self.msg['To'], self.msg.as_string())
        
        server.quit()
        
        print "successfully sent email to %s:" % (self.msg['To'])

    def __init__(self, message_str):
        self.message = message_str
        self.msg = MIMEMultipart()

if __name__ == "__main__":

    test_message = EmailUpdate('Message Test from That Dam Bot')

    test_message.send_email_update()