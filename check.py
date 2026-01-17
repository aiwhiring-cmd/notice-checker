
# ================== CONFIG ==================
URL = "https://erp.aktu.ac.in/Webpages/Public/Circular/CircularForWebsite.aspx"
BOT_TOKEN = "8432608523:AAEJBjMb1qJI_vkNvRBTNQRs0sNSYJTVVWA"
CHAT_ID = "891664539"

CHECK_INTERVAL = 1800  # 30 minutes (DO NOT reduce)
# ============================================

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-IN,en;q=0.9",
    "Referer": "https://erp.aktu.ac.in/",
}

HASH_FILE = "hash.txt"
STATE_FILE = "state.txt"


def send(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg},
            timeout=10
        )
    except:
        pass


def fetch_page():
    for attempt in range(3):
        try:
            r = requests.get(URL, headers=HEADERS, timeout=20)
            r.raise_for_status()
            return r.text
        except Exception as e:
            time.sleep(5)
    return None


def get_hash(html):
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    return hashlib.md5(text.encode()).hexdigest()


# ================== MAIN LOOP ==================
while True:
    now = datetime.now().strftime("%d %b %Y, %I:%M %p")

    html = fetch_page()

    if html is None:
        send(f"ℹ️ AKTU Tracker Update\nWebsite not reachable.\nTime: {now}")
        time.sleep(CHECK_INTERVAL)
        continue

    current_hash = get_hash(html)

    if not os.path.exists(HASH_FILE):
        open(HASH_FILE, "w").write(current_hash)
        send(
            "✅ AKTU Notice Tracker Activated\n"
            f"Monitoring started successfully.\nTime: {now}"
        )
        time.sleep(CHECK_INTERVAL)
        continue

    old_hash = open(HASH_FILE).read()

    if current_hash != old_hash:
        open(HASH_FILE, "w").write(current_hash)
        send(
            "🚨 NEW AKTU NOTICE DETECTED!\n"
            "A new circular/notice has been uploaded.\n"
            f"Time: {now}"
        )

    time.sleep(CHECK_INTERVAL)
