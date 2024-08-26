from time import sleep
from simplegmail import Gmail
import random
import pandas
import datetime
import os

data = pandas.read_csv("startups.csv")
names = data["Name"]
companies = data["Company"]
emails = data["Email"]

gmail = Gmail()  # will open a browser window to ask you to log in and authenticate


# Function to keep track of the last email index sent and the date
def get_last_email_index():
    if os.path.exists("last_email_index.txt"):
        with open("last_email_index.txt", "r") as file:
            content = file.read().split(',')
            last_date = content[0]
            last_index = int(content[1])
            if last_date == str(datetime.date.today()):
                return last_index
            else:
                return -1  # Reset index if the day has changed
    return -1


def set_last_email_index(index):
    with open("last_email_index.txt", "w") as file:
        file.write(f"{str(datetime.date.today())},{index}")


def email_script(name, company):
    lis1_1 = ['hope', 'trust', 'wish']
    lis1_2 = ['finds', 'reaches', 'meets']
    lis1_3 = ['excited', 'thrilled', 'pleased']
    lis1_4 = ['remote work solution', 'remote working option', 'flexible work arrangement']
    lis1_5 = ['backend development', 'server-side development', 'backend engineering']
    lis1_6 = ['quickly pick up', 'rapidly learn', 'swiftly adapt to']
    lis1_7 = ['drive', 'support', 'ensure']
    lis1_8 = ['add value', 'contribute', 'be an asset']
    lis1_9 = ['considering', 'reviewing', 'taking the time to consider']
    lis1_0 = ['Hey', 'Dear', 'Hi']
    script = f"""
        <p>{random.choice(lis1_0)} {name.capitalize()},</p>

        <p>
            I {random.choice(lis1_1)} this email {random.choice(lis1_2)} you well. I recently learned about your {company.capitalize()}'s successful funding round and was {random.choice(lis1_3)} to hear about your growth plans. I am writing to express my interest in joining your team as a Software Engineer.
        </p>

        <p>
            Based in Nigeria, I offer a {random.choice(lis1_4)} that is both cost-effective and efficient. With my experience in {random.choice(lis1_5)}, mobile development, and API integrations, combined with my ability to {random.choice(lis1_6)} new tech stacks, I am confident in my ability to contribute to your projects and help {random.choice(lis1_7)} your success.
        </p>

        <p>
            Please find my CV attached for your review. I would love the opportunity to discuss how I can {random.choice(lis1_8)} to your team.
        </p>

        <p>
            Thank you for {random.choice(lis1_9)} my application.
        </p>

        <p>
            Best regards,<br>
            Elelu Abdulkareem Ayomikun<br>
            <a href="https://www.linkedin.com/in/abdulkareem-elelu-8174b1237/" target="_blank">LinkedIn Profile</a> | +2349023058977
        </p>
    """
    return script


# Get the last email index sent today
start_index = get_last_email_index() + 1

# Send 10 emails
for i in range(start_index, start_index + 10):
    if i < len(companies):
        params = {
            "to": f"{emails[i]}",
            "sender": "Abdulkareem <eleluabdulkareem@gmail.com>",
            "subject": f"Remote Software Engineer at {companies[i]}",
            "msg_html": email_script(names[i], companies[i]),
            "attachments": ["resume.pdf"],
            "signature": True  # use my account signature
        }
        message = gmail.send_message(**params)
        print(f"Application successfully sent to {companies[i]}")
        set_last_email_index(i)
        sleep(300)  # Sleep for 5 minutes between sending each email
