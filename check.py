import requests, hashlib
from bs4 import BeautifulSoup

URL = "https://aktu.ac.in/circulars.html"
BOT_TOKEN = "8432608523:AAEJBjMb1qJI_vkNvRBTNQRs0sNSYJTVVWA"
CHAT_ID = "891664539"

def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )

html = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}).text
soup = BeautifulSoup(html, "html.parser")

content = soup.get_text()
current_hash = hashlib.md5(content.encode()).hexdigest()

try:
    old_hash = open("hash.txt").read()
except:
    old_hash = ""

if current_hash != old_hash:
    send("🚨 New notice uploaded!")
    open("hash.txt", "w").write(current_hash)
