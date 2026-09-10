import os
import time
import requests
import schedule
from bs4 import BeautifulSoup
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# --- 1. SERVER WEB PENTRU RENDER (Gratuit) ---
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write("Botul Pro TV rulează cu succes!".encode("utf-8"))

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    print(f"Serverul web a pornit pe portul {port}")
    server.serve_forever()

# Pornim serverul web pe un fir de execuție separat (background)
threading.Thread(target=run_web_server, daemon=True).start()


# --- 2. CONFIGURARE DISCORD WEBHOOK ---
# Înlocuiește link-ul de mai jos cu URL-ul tău real de Webhook din Discord
DISCORD_WEBHOOK_URL = "PUNE_AICI_LINKUL_TĂU_DE_WEBHOOK"


# --- 3. LOGICA DE SCRAPING PRO TV ȘI TRIMITERE PE DISCORD ---
def trimite_filme_protv():
    url = "https://www.cinemagia.ro/program-tv/pro-tv/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Eroare la accesarea Cinemagia: {response.status_code}")
            return

        soup = BeautifulSoup(response.content, "html.parser")
        randuri = soup.select("tr")
        filme = []

        for rand in randuri:
            ora_elem = rand.select_one(".ora, td:nth-child(1)")
            titlu_elem = rand.select_one(".titlu, td:nth-child(2)")

            if ora_elem and titlu_elem:
                ora = ora_elem.get_text(strip=True)
                titlu = titlu_elem.get_text(strip=True)
                filme.append(f"⏰ **{ora}** - {titlu}")

        if not filme:
            mesaj = "📺 **Program Pro TV**: Nu am găsit filme sau emisiuni în programul de azi."
        else:
            lista_filme = "\n".join(filme[:15]) # Prinde primele 15 intrări
            mesaj = f"📺 **Programul Pro TV de Astăzi**:\n\n{lista_filme}"

        # Trimitere către Discord
        payload = {"content": mesaj}
        res = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        
        if res.status_code in [200, 204]:
            print("Mesajul a fost trimis cu succes pe Discord!")
        else:
            print(f"Eroare la trimiterea pe Discord: {res.status_code}")

    except Exception as e:
        print(f"A apărut o eroare: {e}")


# --- 4. PROGRAMARE ZILNICĂ ---
# Programează trimiterea în fiecare zi la ora 09:00 (sau poți schimba ora)
schedule.every().day.at("09:00").do(trimite_filme_protv)

print("Botul a fost inițializat și așteaptă ora programată...")

# Trimitere de test la pornire pentru a verifica dacă funcționează imediat
# (Opțional: șterge linia de mai jos dacă nu vrei mesaj la fiecare repornire)
trimite_filme_protv()

while True:
    schedule.run_pending()
    time.sleep(60)
