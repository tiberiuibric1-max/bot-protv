import requests
from bs4 import BeautifulSoup
import schedule
import time

# Înlocuiește cu URL-ul Webhook-ului tău din Discord
WEBHOOK_URL = "https://discord.com/api/webhooks/TU_WEBHOOK_AICI"

def trimite_program():
    # Exemplu de structură pentru trimiterea mesajului
    mesaj = {
        "content": "📺 **PROGRAM FILME PRO TV - ASTĂZI** 🍿\n\nProgramul a fost actualizat automat!"
    }
    requests.post(WEBHOOK_URL, json=mesaj)

# Programează trimiterea în fiecare zi la ora 09:00
schedule.every().day.at("09:00").do(trimite_program)

while True:
    schedule.run_pending()
    time.sleep(60)
