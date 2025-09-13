import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from email.mime.text import MIMEText
from configs.config import parameter
from datetime import datetime
COMMASPACE = ', '
MAILER_TEXT = """
Доброго дня. Сьогоднішні пеленги в додатку.

З повагою,
Літик
"""


class MailSender:
    def __init__(self, sender_credits, recipients_lst):
        self.sender_credits = sender_credits
        self.recipients_lst = recipients_lst

    def send_mail(self, subject, text, files=None,
                  server="127.0.0.1"):

        msg = MIMEMultipart()
        msg['From'] = self.sender_credits["user"]
        msg['To'] = COMMASPACE.join(self.recipients_lst)
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject

        msg.attach(MIMEText(text))

        for f in files or []:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)


        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.login(self.sender_credits["user"], self.sender_credits["pwd"])
        smtpserver.sendmail(self.sender_credits["user"], self.recipients_lst, msg.as_string())
        smtpserver.close()



if __name__ == "__main__":
    files = ["/home/peter/Downloads/Звіт_16_05_2025-16_11.kmz"]
    ddic = parameter["mailer"]
    sender = MailSender(ddic, ["pn_romanets@yahoo.com"])
    sender.send_mail(f"Запрошення на змагання", MAILER_TEXT, files)
