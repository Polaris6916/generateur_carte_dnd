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
    #Ouverture du fichier json
    with open('server/data/spells.json', 'r', encoding='utf-8') as spells:
        data = json.load(spells) #Transformation en dictionaire et liste python

    spells_choisie = [] #Liste pour les sorts choisie

    #Lecture des sorts
    for dictionaire in data :
        if dictionaire[type][0] == True and dictionaire[type][1] != None:
            spells_choisie.append(dictionaire) #Ajoute ce que l'on veut

    return(spells_choisie)


def generer_pdf(type, pages, id):
    # Ouvrir le fichier PDF existant
    doc = fitz.open(f"server/data/sort/{type}.pdf")
    output = f"server/temp/{type}_{id}.pdf"

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
    first_image_path = f"server/temp/temp_first_page_{id}.png"
    first_pix.save(first_image_path)

    # Ajouter des pages spécifiques au nouveau fichier PDF
    pages_a_extraire = [int(p) for p in pages.split('-') if p]
    for i, page_num in enumerate(pages_a_extraire):
        if i % 9 == 0 and i != 0:
            c.showPage()  # Créer une nouvelle page après chaque groupe de 9 pages

            for j in range(9):
                # Calculer la position de l'image sur la feuille
                x_first = (j % 3) * (page_width + marge_x) + marge_x
                y_first = height - ((j // 3 % 3 + 1) * (page_height + marge_y))

                # Dessiner l'image sur le canevas sans redimensionnement
                c.drawImage(first_image_path, x_first, y_first, width=first_pix.width / zoom, height=first_pix.height / zoom)

                if j % 9 == 8:
                    c.showPage()

        # Extraire la page et la convertir en image avec une résolution plus élevée
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=mat)
        image_path = f"server/temp/temp_page_{page_num}_{id}.png"
        pix.save(image_path)

        # Calculer la position de l'image sur la feuille
        x = (i % 3) * (page_width + marge_x) + marge_x
        y = height - ((i // 3 % 3 + 1) * (page_height + marge_y))

        # Dessiner l'image sur le canevas sans redimensionnement
        c.drawImage(image_path, x, y, width=pix.width / zoom, height=pix.height / zoom)

        # Supprimer le fichier temporaire
        os.remove(image_path)

    # Ajouter les pages de la première page à la fin si nécessaire
    remaining_pages = len(pages_a_extraire) % 9
    if remaining_pages == 0:
        remaining_pages = 9
    c.showPage()
    for j in range(remaining_pages):
        x_first = (j % 3) * (page_width + marge_x) + marge_x
        y_first = height - ((j // 3 % 3 + 1) * (page_height + marge_y))
        c.drawImage(first_image_path, x_first, y_first, width=first_pix.width / zoom, height=first_pix.height / zoom)
        if j % 9 == 8:
            c.showPage()

    c.save()
    os.remove(first_image_path)
