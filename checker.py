import requests
from bs4 import BeautifulSoup
import time

# Liste des résidences à surveiller
RESIDENCES = [
    {
        "nom": "Simone de Beauvoir",
        "url": "https://www.fac-habitat.com/fr/residences-etudiantes/id-23-simone-de-beauvoir"
    },
    {
        "nom": "Résidence 2",
        "url": "https://www.fac-habitat.com/fr/residences-etudiantes/id-XX-residence-2"
    },
    # Ajoute autant que tu veux
]

CHECK_INTERVAL = 300  # 5 minutes
TOPIC = "logement-fac-habitat"

def notify(message):
    try:
        requests.post(f"https://ntfy.sh/{TOPIC}", data=message.encode())
    except Exception as e:
        print(f"Erreur notification: {e}")

def check_button(url, nom):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers)
        print(f"Vérification de {nom} - Status code: {response.status_code}")
        if response.status_code != 200:
            print(f"Erreur HTTP sur {nom}: {response.status_code}")
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')
        bouton = soup.find("a", class_="btn_reserver", string="Déposer une demande")
        if bouton:
            message = f"✅ Le bouton 'Déposer une demande' est DISPONIBLE à {nom} !"
            notify(message)
            print(message)
        else:
            print(f"❌ Toujours indisponible à {nom}.")
    except Exception as e:
        print(f"Erreur lors de la vérification de {nom} : {e}")

if __name__ == "__main__":
    print("🔍 Checker démarré !")
    while True:
        for residence in RESIDENCES:
            check_button(residence["url"], residence["nom"])
        time.sleep(CHECK_INTERVAL)
