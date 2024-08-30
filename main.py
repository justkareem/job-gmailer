import random
import pandas as pd
import datetime
import os
from time import sleep
from simplegmail import Gmail


def initialize_gmail_objects(sender_creds):
    gmail_objects = []
    for creds in sender_creds:
        gmail = Gmail(creds_file=creds["creds_file"])
        gmail_objects.append({
            "gmail": gmail,
            "sender_email": creds["sender_email"]
        })
    return gmail_objects


def get_last_email_index():
    if os.path.exists("last_email_index.txt"):
        with open("last_email_index.txt", "r") as file:
            content = file.read().split(',')
            last_date = content[0]
            last_index = int(content[1])
            if last_date == str(datetime.date.today()):
                return last_index
            else:
                return last_index  # Reset index if the day has changed
    return -1


def set_last_email_index(index):
    with open("last_email_index.txt", "w") as file:
        file.write(f"{str(datetime.date.today())},{index}")


def email_script(name, company, location):
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

    script = f"""<p>{random.choice(lis1_0)} {name.capitalize()},</p>
        <p>I {random.choice(lis1_1)} this email {random.choice(lis1_2)} you well. I recently learned about your {company.capitalize()}'s successful funding round and was {random.choice(lis1_3)} to hear about your growth plans. I am writing to express my interest in joining your team as a Software Engineer.</p>
        <p>Based in Nigeria, I offer a remote work solution that would cost less than 50% of what you'd typically pay for a software engineer in {location}. With my extensive experience in full stack development, {random.choice(lis1_5)}, mobile app development, and API integrations, combined with my ability to {random.choice(lis1_6)} new tech stacks, I am confident that I can deliver high-quality work at a fraction of the usual cost.</p>
        <p>Please find my CV attached for your {random.choice(["review", "consideration"])}. I would love the opportunity to discuss how I can {random.choice(lis1_8)} to your team, even if you're not actively hiring.</p>
        <p>Thank you for {random.choice(lis1_9)} my application.</p>
        <p>Best regards,<br>Elelu Abdulkareem Ayomikun<br><a href="https://www.linkedin.com/in/abdulkareem-elelu-8174b1237/" target="_blank">LinkedIn Profile</a> | +2349023058977</p>"""
    return script


class EmailSender:
    def __init__(self, data_file, sender_creds):
        self.data = pd.read_csv(data_file)
        self.names = self.data["Name"]
        self.companies = self.data["Company"]
        self.emails = self.data["Email"]
        self.locations = self.data["HQ"]
        self.gmail_objects = initialize_gmail_objects(sender_creds)

    def send_emails(self, start_index, num_emails=10):
        for i in range(start_index, start_index + num_emails):
            if i < len(self.companies):
                gmail_obj = random.choice(self.gmail_objects)
                gmail = gmail_obj["gmail"]
                sender_email = gmail_obj["sender_email"]

                params = {
                    "to": self.emails[i],
                    "sender": sender_email,
                    "subject": f"Remote Software Engineer at {self.companies[i]}",
                    "msg_html": email_script(self.names[i], self.companies[i], self.locations[i]),
                    "attachments": ["resume.pdf"],
                    "signature": True  # use account signature
                }
                message = gmail.send_message(**params)
                print(f"Application successfully sent to {self.companies[i]} from {sender_email}")
                set_last_email_index(i)
                sleep(300)  # Sleep for 5 minutes between sending each email


if __name__ == "__main__":
    sender_creds = [
        {"creds_file": "gmail_token(justkareem).json", "sender_email": "Abdulkareem <justkareemelelu@gmail.com>"},
        {"creds_file": "gmail_token_mss.json", "sender_email": "Abdulkareem <mss.abdulkareem.elelu@tau.edu.ng>"},
        {"creds_file": "gmail_token(eleluabdulkareem).json", "sender_email": "Abdulkareem Elelu <eleluabdulkareem@gmail.com>"},
        # Add more sender credentials and emails if needed
    ]

    email_sender = EmailSender("startups (1).csv", sender_creds)
    start_index = get_last_email_index() + 1
    email_sender.send_emails(start_index, 10)
