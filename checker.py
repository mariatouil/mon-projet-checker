import requests
from bs4 import BeautifulSoup
import time

URL = "https://www.fac-habitat.com/fr/residences-etudiantes/id-23-simone-de-beauvoir"
CHECK_INTERVAL = 300  # 5 minutes

# Remplace "ton-topic-ntfy" par ton nom de topic ntfy personnel
TOPIC = "logement-fac-habitat"

def notify(message):
    # Envoie une notif via ntfy.sh
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
            print("Notification envoyée.")
        else:
            print("❌ Toujours indisponible.")
    except Exception as e:
        print(f"Erreur : {e}")

if __name__ == "__main__":
    while True:
        check_button()
        time.sleep(CHECK_INTERVAL)
