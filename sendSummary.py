import yagmail
import os

from config import root
from config import emails

with open(os.path.join(root, "gmail.cred"), "r") as f:
    username, password = f.read().splitlines()

with open(os.path.join(root, "summaryResults.html", "r")) as f:
    contents = f.read()


yag = yagmail.SMTP(username, password)

for email in emails:
    print(f"Sending email to {email}")
    yag.send(email, 'Daily arXiv Breif', contents)


