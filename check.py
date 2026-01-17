
import requests
import hashlib
from bs4 import BeautifulSoup
import os
import time

URL = "https://erp.aktu.ac.in/Webpages/Public/Circular/CircularForWebsite.aspx"
BOT_TOKEN = "8432608523:AAEJBjMb1qJI_vkNvRBTNQRs0sNSYJTVVWA"
CHAT_ID = "891664539"

def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg},
        timeout=10
    )

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-IN,en;q=0.9",
    "Referer": "https://erp.aktu.ac.in/"
}

try:
    response = requests.get(URL, headers=headers, timeout=15)
    response.raise_for_status()
except Exception as e:
    print("Website not reachable:", e)
    exit(0)   # IMPORTANT: do not fail the action

soup = BeautifulSoup(response.text, "html.parser")
content = soup.get_text()
current_hash = hashlib.md5(content.encode()).hexdigest()

old_hash = open("hash.txt").read() if os.path.exists("hash.txt") else ""

if current_hash != old_hash:
    send("🚨 AKTU: New circular / notice uploaded!")
    open("hash.txt", "w").write(current_hash)

