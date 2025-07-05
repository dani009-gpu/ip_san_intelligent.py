from flask import Flask, request
import requests
from io import StringIO
import sys

app = Flask(__name__)

# Configuration et clés API (à remplacer par vos clés)
IPINFO_KEY =  "671b5d6e64bd60" # Obtenez-la sur ipinfo.io

def generate_page(ip=None, data=None, map_link=None):
    """Génère toute la page HTML en Python pur"""
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>IP Tracker</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; }}
        .container {{ background: #f5f5f5; padding: 20px; border-radius: 10px; }}
        input, button {{ padding: 8px; width: 100%; margin: 5px 0; }}
        button {{ background: #4CAF50; color: white; border: none; cursor: pointer; }}
        .result {{ margin-top: 20px; background: white; padding: 15px; border-radius: 5px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🌍 IP Tracker Simplifié</h1>
        
        <form method="POST">
            <input type="text" name="ip" placeholder="8.8.8.8" required>
            <button type="submit">Chercher</button>
        </form>
    """

    if ip:
        html += f"""
        <div class="result">
            <h2>Résultats pour {ip}</h2>
            <p><strong>Pays:</strong> {data.get('country', 'Inconnu')}</p>
            <p><strong>Ville:</strong> {data.get('city', 'Inconnu')}</p>
            <p><strong>Fournisseur:</strong> {data.get('org', 'Inconnu')}</p>
        """
        
        if map_link:
            html += f'<p><a href="{map_link}" target="_blank">📍 Voir sur la carte</a></p>'
        
        html += "</div>"
    
    html += "</div></body></html>"
    return html

@app.route('/', methods=['GET', 'POST'])
def index():
    ip = data = map_link = None
    
    if request.method == 'POST':
        ip = request.form['ip']
        
        try:
            # Appel API
            response = requests.get(f"https://ipinfo.io/{ip}/json?token={IPINFO_KEY}")
            data = response.json()
            
            # Création lien carte
            if 'loc' in data:
                lat, lon = data['loc'].split(',')
                map_link = f"https://maps.google.com/?q={lat},{lon}"
                
        except Exception as e:
            print(f"Erreur: {e}", file=sys.stderr)
    
    return generate_page(ip, data, map_link)

if __name__ == '__main__':
    app.run(debug=True)