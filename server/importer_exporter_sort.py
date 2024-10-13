import json
import os
import fitz  # PyMuPDF
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def selection_sort(type):
    """Permet de créer/modier le fichier json spells_choisie.json pour le triés selon la classe de notre personnage

    Args:
        type (str): le type de lanceur de sort choisie
    """
    chemin_repertoire_courant = recuper_chemin_absolue()
    #Ouverture du fichier json
    with open(chemin_repertoire_courant + '/data/spells.json', 'r', encoding='utf-8') as spells:
        data = json.load(spells) #Transformation en dictionaire et liste python

    spells_choisie = [] #Liste pour les sorts choisie

    #Lecture des sorts
    for dictionaire in data :
        if dictionaire[type][0] == True and dictionaire[type][1] != None:
            spells_choisie.append(dictionaire) #Ajoute ce que l'on veut

    return(spells_choisie)


def generer_pdf(type, pages, id):
    chemin_repertoire_courant = recuper_chemin_absolue()
    # Ouvrir le fichier PDF existant
    doc = fitz.open(f"{chemin_repertoire_courant}/data/sort/{type}.pdf")
    output = f"{chemin_repertoire_courant}/temp/{type}_{id}.pdf"

    # Créer un nouveau PDF avec ReportLab
    c = canvas.Canvas(output, pagesize=A4)
    width, height = A4

    # Définir les marges et les dimensions pour 9 pages par feuille
    marge_x = 10  # Marge horizontale
    marge_y = 10  # Marge verticale
    page_width = (width - 4 * marge_x) / 3
    page_height = (height - 4 * marge_y) / 3

    # Extraire la première page une fois pour réutilisation
    first_page = doc.load_page(0)
    zoom = 6  # Facteur de zoom pour augmenter la résolution
    mat = fitz.Matrix(zoom, zoom)
    first_pix = first_page.get_pixmap(matrix=mat)
    first_image_path = f"{chemin_repertoire_courant}/temp/temp_first_page_{id}.png"
    first_pix.save(first_image_path)

    # Ajouter des pages spécifiques au nouveau fichier PDF
    pages_a_extraire = [int(p) for p in pages.split('-') if p]
    for i, page_num in enumerate(pages_a_extraire):
        if i % 9 == 0 and i != 0:
            # Ajouter une page avec la première page répétée 9 fois
            c.showPage()
            for j in range(9):
                # Calculer la position de l'image sur la feuille
                img_width = first_pix.width / zoom
                img_height = first_pix.height / zoom
    
                x_first = (j % 3) * (page_width + marge_x) + marge_x + (page_width - img_width) / 2
                y_first = height - ((j // 3 % 3 + 1) * (page_height + marge_y)) + (page_height - img_height) / 2

                # Dessiner l'image sur le canevas sans redimensionnement
                c.drawImage(first_image_path, x_first, y_first, width=first_pix.width / zoom, height=first_pix.height / zoom)

            c.showPage()  # Commencer une nouvelle page après le groupe de 9 cartes et la première page répétée

        # Extraire la page et la convertir en image avec une résolution plus élevée
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=mat)
        image_path = f"{chemin_repertoire_courant}/temp/temp_page_{page_num}_{id}.png"
        pix.save(image_path)

        # Calculer la taille réelle de l'image après redimensionnement
        img_width = pix.width / zoom
        img_height = pix.height / zoom

        # Calculer la position centrée de l'image
        x = (i % 3) * (page_width + marge_x) + marge_x + (page_width - img_width) / 2
        y = height - ((i // 3 % 3 + 1) * (page_height + marge_y)) + (page_height - img_height) / 2

        # Dessiner l'image sur le canevas centrée
        c.drawImage(image_path, x, y, width=img_width, height=img_height)

        # Supprimer le fichier temporaire
        os.remove(image_path)

    # Gérer les cartes restantes après le dernier groupe complet de 9 pages
    remaining_pages = len(pages_a_extraire) % 9
    if remaining_pages % 3 == 1 :
        c.showPage()
        for j in range(remaining_pages):
            if remaining_pages - j >= 3 :
                img_width = first_pix.width / zoom
                img_height = first_pix.height / zoom

                x_first = (j % 3) * (page_width + marge_x) + marge_x + (page_width - img_width) / 2
                y_first = height - ((j // 3 % 3 + 1) * (page_height + marge_y)) + (page_height - img_height) / 2

                # Dessiner la première image centrée pour le dernier groupe
                c.drawImage(first_image_path, x_first, y_first, width=img_width, height=img_height)
            
            elif remaining_pages - j > 0:
                img_width = first_pix.width / zoom
                img_height = first_pix.height / zoom

                x_first = ((j % 3) * (page_width + marge_x) + marge_x + (page_width - img_width) / 2)
                y_first = height - ((j // 3 % 3 + 1) * (page_height + marge_y)) + (page_height - img_height) / 2

                x_inverted = width - (x + img_width)

                # Dessiner la première image centrée pour le dernier groupe
                c.drawImage(first_image_path, x_inverted, y_first, width=img_width, height=img_height)

    elif remaining_pages % 3 == 2 :
        c.showPage()
        for j in range(remaining_pages+1):
            if remaining_pages - j >= 3 or remaining_pages -j <= 1:
                img_width = first_pix.width / zoom
                img_height = first_pix.height / zoom

                x_first = (j % 3) * (page_width + marge_x) + marge_x + (page_width - img_width) / 2
                y_first = height - ((j // 3 % 3 + 1) * (page_height + marge_y)) + (page_height - img_height) / 2

                # Dessiner la première image centrée pour le dernier groupe
                c.drawImage(first_image_path, x_first, y_first, width=img_width, height=img_height)

        c.showPage()  # Finir le groupe incomplet de 9 pages

    elif remaining_pages % 3 == 0 :
        c.showPage()
        for j in range(remaining_pages):
            img_width = first_pix.width / zoom
            img_height = first_pix.height / zoom
            x_first = (j % 3) * (page_width + marge_x) + marge_x + (page_width - img_width) / 2
            y_first = height - ((j // 3 % 3 + 1) * (page_height + marge_y)) + (page_height - img_height) / 2
            
            c.drawImage(first_image_path, x_first, y_first, width=img_width, height=img_height)

    # Sauvegarder le fichier PDF final
    c.save()
    os.remove(first_image_path)

def recuper_chemin_absolue():
    """Fonction qui permet de récupérer le chemin absolue pour le système. Suivant le OS le répertoire courant n'est pas le même.
    La fonction regarde si on est dans le répertoire server. Si oui ne fait rien sinon le rajoute

    Returns:
        str: Chemin absolue des fichiers
    """
    chemin = os.getcwd()
    if len(chemin) >=7:
        chemin_relatif = chemin[len(chemin)-7:]
        if chemin_relatif != "/server" :
            chemin += "/server"
    else :
        chemin += "/server"
    
    if not os.path.exists(chemin + "/temp"):
        os.makedirs(chemin + "/temp")
    
    return chemin