import smtplib
from os.path import basename
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64


class Notify:
    def __init__(self, server, username, passwd, port=465):
        self.server = smtplib.SMTP_SSL(server, port)
        self.smtp_server = server
        self.port = port
        self.username = username
        self.passwd = passwd

    def send_email(self, rcpt, sender, subject, message, name_sender='', attach_file=None):
        # self.server.set_debuglevel(1)
        self.server.login(self.username, self.passwd)
        # add header
        self.msg = MIMEMultipart()
        self.msg['From'] = '"{}" <{}>'.format(name_sender, sender)
        self.msg['To'] = rcpt
        self.msg['Subject'] = subject
        # add attachment
        if attach_file:
            self.attch = MIMEBase('application', "octet-stream")
            self.attch.set_payload(open(attach_file, 'rb').read())
            encode_base64(self.attch)
            self.attch.add_header(
                'Content-Disposition',
                'attachment',
                filename=basename(attach_file)
            )
            self.msg.attach(self.attch)
        # add message text
        self.msg.attach(MIMEText(message))
        # send email
        self.server.sendmail(sender, rcpt, self.msg.as_string())
        self.server.quit()
