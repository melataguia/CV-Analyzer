import requests

# URL de ton API Flask
url = "http://127.0.0.1:5000/parse"

# Ouvrir le fichier CV en mode binaire
with open('cv.pdf', 'rb') as file:
    files = {'cv': file}
    
    try:
        # Envoi de la requête POST à l'API
        response = requests.post(url, files=files)

        # Vérifier si la requête a réussi
        if response.status_code == 200:
            print("Status code:", response.status_code)
            print("Response:", response.json())  # Affiche le résultat du traitement du CV
        else:
            print(f"Erreur : {response.status_code}")
            print("Détails de l'erreur:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"Une erreur est survenue lors de l'envoi de la requête : {e}")
