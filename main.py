
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import os

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

URL = "https://jo.opensooq.com/ar/لابتوب-وكمبيوتر/all"
CHECK_INTERVAL = 300  # 5 دقائق
seen_ads = set()

def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())

def check_new_ads():
    global seen_ads
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")
    ads = soup.find_all("a", class_="sc-dznXNo fqwxvA")
    new_ads = []
    
    for ad in ads:
        title = ad.get_text(strip=True)
        link = "https://jo.opensooq.com" + ad.get("href")
        if link not in seen_ads:
            seen_ads.add(link)
            new_ads.append((title, link))
    
    return new_ads

if __name__ == "__main__":
    while True:
        print("🔄 جاري التحقق من الإعلانات الجديدة...")
        new_ads = check_new_ads()
        if new_ads:
            for title, link in new_ads:
                send_email("📢 إعلان جديد على السوق المفتوح", f"{title}
{link}")
                print(f"📬 إعلان جديد: {title}")
        else:
            print("❌ لا يوجد إعلانات جديدة هذه المرة.")
        time.sleep(CHECK_INTERVAL)
