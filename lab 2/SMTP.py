import smtplib
from email.mime.text import MIMEText

def send_email():
    sender = "hello@demomailtrap.co"
    receiver = "siddharthareddyiitp@gmail.com"
    username = "api"
    password = "<YOUR_API_TOKEN>"   

    msg = MIMEText("Hello Siddhartha, this is a test email via Mailtrap.")
    msg["Subject"] = "CN Lab 2 - SMTP Test"
    msg["From"] = sender
    msg["To"] = receiver

    try:
        s = smtplib.SMTP("live.smtp.mailtrap.io", 587)
        s.starttls()
        s.login(username, password)
        s.sendmail(sender, receiver, msg.as_string())
        s.quit()
        print("Email sent successfully.")
    except Exception as e:
        print("Error:", e)

send_email()
