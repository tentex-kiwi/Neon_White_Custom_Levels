import smtplib
from email.mime.text import MIMEText

EMAIL_ADDRESS = "jordan.stinson@gmail.com"
EMAIL_PASSWORD = "lssb ioke oiyv rhea"
TO_EMAIL = "jordan.stinson@gmail.com"

def send_email(subject, body):

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL

    try:

        with smtplib.SMTP_SSL(
            "smtp.gmail.com",
            465
        ) as smtp:

            smtp.login(
                EMAIL_ADDRESS,
                EMAIL_PASSWORD
            )

            smtp.send_message(msg)

        print("Email sent.")

    except Exception as e:

        print(f"Email failed: {e}")

send_email(
    "Machu Picchu Check", "Test email from Machu Picchu check script.")