import imaplib
import configparser
import email
from email.header import decode_header
import logging


class EmailManager:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s [%(levelname)s] - %(name)s - %(message)s',
                    filename="Logs.log")
        self.log = logging.getLogger("EmailDigest")

        self.parser = configparser.ConfigParser()
        self.parser.read('config.ini')

        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
        self.mail.login(
            self.parser['DETAILS']['user'].strip(),
            self.parser['DETAILS']['password'].strip()
        )

    def getBody(self, msg):
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode()
        elif msg.get_content_type() == "text/html":
            return "HTML type"

    def grabEmail(self):
        status, mailbox = self.mail.select("INBOX")
        status, messages = self.mail.search(None, "ALL")
        email_ids = messages[0].split()[::-1]


        for emails in email_ids:
            status, msg_data = self.mail.fetch(emails, '(RFC822)')

            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    try:
                        msg = email.message_from_bytes(response_part[1])
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding if encoding else "utf-8")
                        print(subject)
                        if subject == "test":
                            self.mail.store(emails, '+X-GM-LABELS', "TESTINGLABEL")
                            quit()
                    except AttributeError as ex:
                        print(f"Attribute error occoured: {ex}")
        

# Run it
manager = EmailManager()
manager.grabEmail()
