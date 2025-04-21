# Utilise une image Python slim
FROM python:3.11-slim

# Définit le dossier de travail dans le conteneur
WORKDIR /app

# Copie les dépendances et installe-les
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout le code
COPY . .

# Ouvre le port 5000 (optionnel mais conseillé)
EXPOSE 5000

# Commande de lancement avec waitress
CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "wsgi:app"]