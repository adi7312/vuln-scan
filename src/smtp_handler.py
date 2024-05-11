import email, smtplib, ssl, os

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

receiver_email = os.environ.get("EMAIL")

def send_email(password, text,path_to_report,receiver_email=receiver_email,sender_email="avscontainer@gmail.com"):
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, prepare_email(path_to_report))

def prepare_email(path_to_report,receiver_email=receiver_email,sender_email="avscontainer@gmail.com"):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Results of security scan"
    message.attach(MIMEText("Results of security scan", "plain"))
    message.attach(prepare_report(path_to_report))
    return message.as_string()


def prepare_report(path_to_report):
    with open(path_to_report, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {path_to_report[13:]}",
    )
    return part
    
