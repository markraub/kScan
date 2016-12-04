import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from os.path import basename
import time
import locale


def sendMail(file_name, user):

    attachment = "/scans/" + user + "/" + file_name
    me = "kscan@csh.rit.edu"
    you = user + "@csh.rit.edu"
    text = MIMEText(
        "Your scan is complete! \nIf something is wrong with this email, check out the wiki to learn another way to get your file!")
    msg = MIMEMultipart()
    msg.attach(text)
    f = open(attachment, "rb")
    part = MIMEApplication(f.read(), Name=basename(attachment))
    part["Content-Disposition"] = 'attachment; filename="%s"' % basename(attachment)
    msg.attach(part)
    msg["Subject"] = "Here is your completed scan!"
    msg["From"] = me
    msg["To"] = you
    msg.preamble = "Here is your completed scan!"
    s = smtplib.SMTP('mail.csh.rit.edu')
    s.sendmail(me, you, msg.as_string())
    print("[" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + "] Email message sent")
    s.quit()


def goodbyeMail(user):
    me = "kscan@csh.rit.edu"
    you = user + "@csh.rit.edu"
    msg = MIMEMultipart()
    text = MIMEText("Your scan backup has been deleted, for more info see the wiki")
    msg.attach(text)
    msg["Subject"] = "Scan Backup Deleted"
    msg["From"] = me
    msg["To"] = you
    s = smtplib.SMTP('mail.csh.rit.edu')
    s.sendmail(me, you, msg.as_string())
    print("[" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()) + "] Email message sent")
    s.quit()

if __name__ == "__main__":

    pass

