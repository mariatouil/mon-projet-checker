import requests
from bs4 import BeautifulSoup
import time

# Liste des résidences à surveiller
RESIDENCES = [
    {
        "nom": "Simone de Beauvoir massy",
        "url": "https://www.fac-habitat.com/fr/residences-etudiantes/id-23-simone-de-beauvoir"
    },
    {
        "nom": "Résidence Magellan massy ",
        "url": "https://www.fac-habitat.com/fr/residences-etudiantes/id-77-magellan"
    },
    {
        "nom": "Résidence Erwin Guldner  sceaux ",
        "url": "https://www.fac-habitat.com/fr/residences-etudiantes/id-80-residence-etudiante-erwin-guldner-sceaux"
    },
    {
        "nom": "Résidence pierre-ringenbach-  sceaux ",
        "url": "https://www.fac-habitat.com/fr/residences-etudiantes/id-82-residence-etudiante-pierre-ringenbach-sceaux"
    },
    {
        "nom": "Cesaria Evora aubervillier ",
        "url": "https://www.fac-habitat.com/fr/residences-etudiantes/id-35-cesaria-evora"
    },
    {
        "nom": "Phylosofia aubervillier ",
        "url": "https://www.fac-habitat.com/fr/residences-etudiantes/id-57-philosophiaa"
    },
    {
        "nom": "lucie-aubrac aubervillier ",
        "url": "https://www.fac-habitat.com/fr/residences-etudiantes/id-78-lucie-aubrac"
    },
    
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
        boutons = soup.find_all("a", class_="btn_reserver")
        for bouton in boutons:
            if "déposer une demande" in bouton.text.strip().lower():
                message = f"✅ Le bouton 'Déposer une demande' est DISPONIBLE à {nom} !"
                notify(message)
                print(message)
                return
        
        print(f"❌ Toujours indisponible à {nom}.")
    except Exception as e:
        print(f"Erreur lors de la vérification de {nom} : {e}")


if __name__ == "__main__":
    print("🔍 Checker démarré !")
    while True:
        for residence in RESIDENCES:
            check_button(residence["url"], residence["nom"])
        time.sleep(CHECK_INTERVAL)
