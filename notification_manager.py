import os
from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()

class NotificationManager:
    def __init__(self):
        self.client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_ACCOUNT_SID'])

    def send_message(self, message_body):
        message = self.client.messages.create(
            from_=os.environ["TWILIO_VIRTUAL_NR"],
            body=message_body,
            to=os.environ["TWILIO_VIRTUAL_NR"]
        )
        # Prints if successfully sent.
        print(message.sid)

