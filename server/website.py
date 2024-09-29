#Importation des bibliothèque
from flask import Flask, render_template, jsonify, send_file, after_this_request #Serveur web
from werkzeug.utils import send_from_directory
import os
from dotenv import load_dotenv
from importer_expoter_sort import selection_sort, generer_pdf
from datetime import datetime
import threading

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

app = Flask(__name__)

@app.route("/static/<path:path>") #Route pour les appels des pages statiques
def static_dir(path):
    return send_from_directory("static", path) #il renvoie vers le dossier corespondant

@app.route('/') #Route par défaut lorsque on arrive sur le site sans paramètre
def index():
    return render_template('index.html') #Renvoie l'index.html

@app.route('/spells.html/<string:type>', methods=['GET'])
def sort(type):
    return jsonify(selection_sort(type))

@app.route("/pdf.html/<string:classe>/<string:pages>", methods=['GET'])
def pdf(classe, pages):
    id = datetime.now().strftime("%Y%m%d_%H%M%S")
    generer_pdf(classe, pages, id)
    chemin = f"temp/{classe}_{id}.pdf"

    @after_this_request
    def remove_file(response):
        def delayed_remove():
            try:
                os.remove("server/"+chemin)
                print(f"Fichier supprimé : {chemin}")
            except Exception as e:
                print(f"Erreur lors de la suppression du fichier : {e}")

        threading.Timer(1, delayed_remove).start()
        return response

    return send_file(chemin, as_attachment=True)

# lance le serveur web
print("Start Flask")
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5401)