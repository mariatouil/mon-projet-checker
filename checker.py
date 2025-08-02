import requests
from bs4 import BeautifulSoup
import time

URL = "https://www.fac-habitat.com/fr/residences-etudiantes/id-23-simone-de-beauvoir"
TOPIC = "ton-topic-ntfy"  # remplace par ton nom de topic ntfy
CHECK_INTERVAL = 300  # 5 minutes

def notify(message):
    requests.post(f"https://ntfy.sh/{TOPIC}", data=message.encode())

def check_button():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        bouton = soup.find("a", class_="btn_reserver", string="Déposer une demande")
        if bouton:
            notify("✅ Le bouton 'Déposer une demande' est DISPONIBLE !")
        else:
            print("❌ Toujours indisponible.")
    except Exception as e:
        print(f"Erreur : {e}")

while True:
    check_button()
    time.sleep(CHECK_INTERVAL)
