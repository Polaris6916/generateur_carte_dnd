#Importation des biblothèques
import requests #Permet de faire des requêtes web
from bs4 import BeautifulSoup #Permet de rechercher des éléments dans un texte web
import json #Création de fichier json
from pdfminer.high_level import extract_text
import os

def recuper_chemin_absolue():
    """Fonction qui permet de récupérer le chemin absolue pour le système. Suivant le OS le répertoire courant n'est pas le même.
    La fonction regarde si on est dans le répertoire server. Si oui ne fait rien sinon le rajoute

    Returns:
        str: Chemin absolue des fichiers
    """
    chemin = os.getcwd()
    try :
        chemin_relatif = chemin[len(chemin)-7:]
        if chemin_relatif != "/server" :
            chemin += "/server"
    except :
        chemin += "/server"
    
    return chemin

def extraction_nom_page_sort(pdf_path):
    """Fonction qui permet de extraire le nom ainsi que le numéros de page des cartes de sort

    Args:
        pdf_path (str): le chemin vers le pdf de carte de sort

    Returns:
        dict: le dictionnaire des nom des sorts ainsi que de numeros de page
    """
    pdf_path = recuper_chemin_absolue() + "/"+ pdf_path
    #Extraction du texte et séparation en différente page
    text = extract_text(pdf_path)
    pages = text.split('\f')

    #Supression des page qui ne sont pas des sorts
    del pages[0]
    del pages[-1]

    #Création du dictionnaire final
    sort = {}
    multi_carte = 0
    nom_sort = None

    for page_num, page in enumerate(pages): #Boucle qui fait page par page
        page = page.split('\n')#Séparation des lignes

        if multi_carte > 0 : #Si c'est une multicarte
            multi_carte -= 1
            sort[nom_sort].append(page_num+1)#Ajout de l'autre page à la liste

        else : #Cas normal
            if page[3] == "": #Si le nom est sur qu'une ligne
                nom_sort = page[2] #récupération de se nom
                if page[2][-2] in "123456789": #Permet de voir si la page est sur plusieurs cartes
                    multi_carte = int(page[2][-2])-1 #Permet de voir combien il y a d'autre carte
                    nom_sort = nom_sort[:-6] #Ajout du nom sans celle-ci
                sort[nom_sort] = [page_num+1] #Ajout du sort ainsi que son numéros de page
                    
            else : #Si le nom du sort est sur 2 lignes
                nom_sort = page[2]+page[3] #Ajout du nom complet
                if page[3][-2] in "123456789": #Si le sort est une multicarte
                    multi_carte = int(page[3][-2])-1 #Permet de voir combien il y a d'autre carte
                    nom_sort = nom_sort[:-6] #Ajout du nom sans celle-ci
                sort[nom_sort] = [page_num+1] #Ajout du sort ainsi que son numéros de page

    return sort #Envoie du dictionaire

def exctaction_nom_sort_all():
    """Fonction pour récupérer chaque sort de chaque classe ainsi que son numéros de page

    Returns:
        dict: le dictionnaire complet
    """
    #Initialisation de variable
    sort = {}
    liste_classe = ["barde", "clerc", "druide", "ensorceleur", "magicien", "occultiste", "paladin", "rodeur", "multiclasse"]

    #Permet de faire tout les appels poour récupérer chaque dictionaire de chaque type de classe
    for classe in liste_classe:
        sort[classe] = extraction_nom_page_sort(recuper_chemin_absolue()+"/data/sort/"+classe+".pdf")
    
    #Envoie du dictionaire complet
    return sort

def recuperation_page_classe (page, sort_classe, level, nom, type):
    """Fonction pour permettre de récupérer le numéros de page ainsi que si il est dans le dictionaire des classe

    Args:
        page (dict): dictionnaire des numéros de page
        sort_classe (dict): dictionnaire des sorts de chaque classe
        level (int): niveaux du sort
        nom (str): nom du sort
        type (str): classe du sort

    Returns:
        bool, list: si le sort appartient à la classe du type, 
    """
    corespondance = {
    'Agrandissement/Rapetissement' : 'AGRANDIR/RÉTRÉCIR',
    "Animation d'objets" : "ANIMATION DES OBJETS",
    "Armure de mage" : "ARMURE DU MAGE",
    "Aspersion d'acide" : "ASPERSION ACIDE",
    'Boule de feu à retardement' : "BOULE DE FEU À EXPLOSION RETARDÉE",
    "Chaîne d'éclairs" : "CHAÎNE D’ÉCLAIRS",
    'Métal brûlant' : "CHAUFFER LE MÉTAL",
    'Chien de garde de Mordenkainen' : "CHIEN DE GARDE",
    'Coffre secret de Léomund' : "COFFRE SECRET",
    "Contact avec un autre plan" : "CONTACTER UN AUTRE PLAN",
    "Contrôle de l'eau" : "CONTRÔLE DE L’EAU",
    "Convocations instantanées de Drawmij" : "CONVOCATIONS INSTANTANÉES",
    "Création de nourriture et d'eau" : "CRÉATION DE NOURRITURE ET D’EAU",
    "Création ou destruction d'eau" : "CRÉATION OU DESTRUCTION D’EAU",
    "Croissance d'épines" : "CROISSANCE D’ÉPINES",
    "Danse irrésistible d'Otto" : "DANSE IRRÉSISTIBLE",
    "Disque flottant de Tenser" : "DISQUE FLOTTANT",
    "Domination de bête" : "DOMINER UNE BÊTE",
    "Domination de personne" : "DOMINER UN HUMANOÏDE",
    "Domination de monstre" : "DOMINER UN MONSTRE",
    "Communication à distance" : "ENVOI DE MESSAGE",
    "Épée de Mordenkainen" : "ÉPÉE MAGIQUE",
    "Décharge occulte" : "EXPLOSION OCCULTE",
    "Fléau d'insectes" : "FLÉAU D’INSECTES",
    "Flèche acide de Melf" : "FLÈCHE ACIDE",
    "Fou rire de Tasha" : "FOU RIRE",
    "Globe d'invulnérabilité" : "GLOBE D’INVULNÉRABILITÉ",
    "Immobilisation de monstre" : "IMMOBILISER UN MONSTRE",
    "Immobilisation de personne" : "IMMOBILISER UN  HUMANOÏDE",
    "Invocation d'animaux" : "INVOQUER DES ANIMAUX",
    "Invocation d'élémentaires mineurs" : "INVOQUER DES ÉLÉMENTAIRES MINEURS",
    "Invocation d'êtres sylvestres" : "INVOQUER DES ÊTRES DES BOIS",
    "Invocation de céleste" : "INVOQUER UN CÉLESTE",
    "Invocation de fée" : "INVOQUER UNE FÉE",
    "Lien télépathique de Rary" : "LIEN TÉLÉPATHIQUE",
    "Don des langues" : "LANGUES",
    "Mythes et légendes" : "LÉGENDE",
    "Feuille morte" : "LÉGER COMME UNE PLUME",
    "Délivrance des malédictions" : "LEVER UNE MALÉDICTION",
    "Localisation d'animaux ou de plantes" : "LOCALISER DES ANIMAUX OU DES PLANTES",
    "Localisation d'objet" : "LOCALISER UN OBJET",
    "Localisation de créature" : "LOCALISER UNE CRÉATURE",
    "Lueur d'espoir" : "LUEUR D’ESPOIR",
    "Lueurs féeriques" : "LUEURS FÉÉRIQUES",
    "Main de Bigby" : "MAIN MAGIQUE",
    "Main de mage" : "MAIN DU MAGE",
    "Malédiction" : "JETER UNE MALÉDICTION",
    "Manoir somptueux de Mordenkainen" : "MANOIR SOMPTUEUX",
    "Marche sur l'eau" : "MARCHE SUR L’EAU",
    "Mauvais oeil" : "MAUVAIS ŒIL",
    "Modification d'apparence" : "MODIFIER SON APPARENCE",
    "Mur d'épines" : "MUR D’ÉPINES",
    "Nuage nauséabond": "NUAGE PUANT",
    "Antidétection" : "NON-DÉTECTION",
    "Nuée de dagues" : "NUÉE DE PROJECTILES",
    "Oeil magique" : "ŒIL MAGIQUE",
    "Pattes d'araignée" : "PATTES D’ARAIGNÉE",
    "Portail magique" : "PASSAGE DIMENSIONNEL",
    "Peau d'écorce" : "PEAU D’ÉCORCE",
    "Petite hutte de Léomund" : "PETITE HUTTE",
    "Prière de guérison" : "PRIÈRE DE SOINS",
    "Prévoyance" : "CONTINGENCE",
    "Projection d'image" : "IMAGE PROJETÉE",
    "Protection contre une énergie" : "PROTECTION CONTRE LES ÉNERGIES",
    "Purification de nourriture et d'eau" : "PURIFICATION DE LA NOURRITURE ET DE L’EAU",
    "Restauration partielle" : "RESTAURATION INFÉRIEURE",
    "Retour à la vie" : "REVIGORER",
    "Songe" : "RÊVE",
    "Sanctuaire privé de Mordenkainen" : "SANCTUAIRE PRIVÉ",
    "Soins" : "SOIN DES BLESSURES",
    "Soins de groupe" : "SOIN DES BLESSURES DE GROUPE",
    "Sphère glaciale d'Otiluke" : "SPHÈRE GLACÉE",
    "Sphère résiliente d'Otiluke" : "SPHÈRE RÉSILIENTE",
    "Tentacules noirs d'Evard" : "TENTACULES NOIRS",
    "Toile d'araignée" : "TOILE D’ARAIGNÉE",
    "Sens des pièges" : "TROUVER LES PIÈGES",
    "Sens de l'orientation" : "TROUVER UN CHEMIN",
    "Appel de destrier" : "TROUVER UNE MONTURE",
    "Coup au but" : "VISER JUSTE",
    "Voir l'invisible" : "VOIR L’INVISIBLE",
    "Voie végétale" : "TRANSPORT VÉGÉTAL",
    
}
    
    if type == "multiclasse":
        try :
            return True, page[type][nom.upper()]
        except :
            try :
                return True, page[type][corespondance[nom]]
            except :
                return False, None
    else :
        try:
            page = page[type][nom.upper()]
            return (nom.lower() in sort_classe[type][int(level)]), page
        except:
            try:
                return (nom.lower() in sort_classe[type][int(level)]), page[type][corespondance[nom]]
            except :
                return False, None

def scrapping_sort():
    """Permet de récupérer les sorts de dnd 5e pour les ajouter dans un fichier json
    """
    #Envoie et récupere la page web des sort
    url = 'https://www.aidedd.org/dnd-filters/sorts.php'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser') #Permet comprendre l'html
    sort_classe = { #Dictionnaire avec les sorts de chaque classe lanceur de sort (sauf guerrier)
        "barde" : [
            ["coup au but","faux amis illusion mineure","lumière lumières dansantes","main du mage","message","moquerie cruelle","prestidigitation","protection contre les armes","réparation"],
            ["amitié avec les animaux","charme-personne","communication avec les animaux","compréhension des langues","déguisement","détection de la magie","feuille morte","fou rire de Tasha","grande foulée","héroïsme","identification","image silencieuse","imprécation","lueurs féeriques","mot de guérison","murmures dissonants","serviteur invisible","soins","sommeil","texte illusoire","vague tonnante"],
            ["amélioration de caractéristique","apaisement des émotions","couche magique","cité/surdité","couronne du dément","déblocage","détection de l'invisibilité","détection des pensées","discours captivant","immobilisation de personne","invisibilité","force fantasmagorique","fracassement","localisation d'animaux ou de plantes","localisation d'objet","messager animal","métal brûlant","nuée de dagues","restauration partielle","silence","suggestion","zone de vérité"],
            ["antidétection","clairvoyance","communication à distance","communication avec les morts","communication avec les plantes","croissance végétale","dissipation de la magie","don des langues","état cadavérique","glyphe de garde","image majeure","malédiction","motif hypnotique","nuage nauséabond","petite hutte de Léomund","terreur"],
            ["compulsion","confusion","invisibilité suprême","liberté de mouvement","localisation de créature","métamorphose","porte dimensionnelle","terrain hallucinatoire"],
            ["animation des objets","apparence trompeuse","cercle de téléportation","domination de personne","double illusoire","entrave planaire","éveil","immobilisation de monstre","modification de mémoire","mythes et légendes","quête","rappel à la vie","restauration suprême","scrutation","soins de groupe","songe"],
            ["danse irrésistible d'Otto","illusion programmée","mauvais œil","orientation","protections et sceaux","suggestion de groupe","vision suprême"],
            ["cage de force","épée de Mordenkainen","forme éthérée","image projetée","manoir somptueux de Mordenkainen","mirage","régénération","résurrection","symbole","téléportation"],
            ["bagou","domination de monstre","esprit faible","esprit impénétrable","mot de pouvoir étourdissant"],
            ["métamorphose suprême", "mot de pouvoir guérisseur", "mot de pouvoir mortel", "prémonition"]],
        "clerc" : [
            ["assistance","flamme sacrée","lumière","réparation","résistance","stabilisation","thaumaturgie"], 
            ["bénédiction","blessure","bouclier de la foi","création ou destruction d'eau","détection de la magie","détection du mal et du bien","détection du poison et des maladies","imprécation","injonction","mot de guérison","protection contre le mal et le bien","purification de la nourriture et de l'eau","rayon traçant","sanctuaire","soins"], 
            ["aide","amélioration de caractéristique","apaisement des émotions","arme spirituelle","augure","cécité/surdité","détection des pièges","doux repos","flamme éternelle","immobilisation de personne","lien de protection","localisation d'objet","prière de guérison","protection contre le poison","restauration partielle","silence","zone de vérité"], 
            ["animation des morts","cercle magique","clairvoyance","communication à distance","communication avec les morts","création de nourriture et d'eau","délivrance des malédictions","dissipation de la magie","don des langues","esprits gardiens","état cadavérique","fusion dans la pierre","glyphe de garde","lueur d'espoir","lumière du jour","malédiction","marche sur l'onde","mot de guérison de groupe","protection contre l'énergie","retour à la vie"], 
            ["bannissement","contrôle de l'eau","divination","façonnage de la pierre","gardien de la foi","liberté de mouvement","localisation de créature","protection contre la mort"], 
            ["colonne de flamme","communion","contagion","dissipation du mal et du bien","entrave planaire","fléau d'insectes","mythes et légendes","quête","rappel à la vie","restauration suprême","sanctification","scrutation","soins de groupe"], 
            ["allié planaire","barrière de lames","contamination","création de mort-vivant","festin des héros","guérison","interdiction","mot de retour","orientation","vision suprême"],
            ["changement de plan","forme éthérée","invocation de céleste","parole divine","régénération","résurrection","symbole","tempête de feu"], 
            ["aura sacrée","champ antimagie","contrôle du climat","tremblement de terre"], 
            ["guérison de groupe","portail","projection astrale","résurrection suprême"]],
        "druide" : [
            [ "assistance", "bouffée de poison", "crosse des druides", "druidisme", "flammes", "fouet épineux", "réparation", "résistance"],
            ["amitié avec les animaux", "baies nourricières", "charme-personne", "communication avec les animaux", "création ou destruction d'eau", "détection de la magie", "détection du poison et des maladies", "enchevêtrement", "grande foulée", "lueurs féeriques", "mot de guérison", "nappe de brouillard", "purification de la nourriture et de l'eau", "saut", "soins", "vague tonnante"],
            ["amélioration de caractéristique","bourrasque","croissance d'épines","détection des pièges","immobilisation de personne","lame de feu","localisation d'animaux ou de plantes","localisation d'objet","messager animal","métal brûlant","passage sans trace","peau d'écorce","protection contre le poison","rayon de lune","restauration partielle","sens animal","sphère de feu","vision dans le noir"],
            ["appel de la foudre","communication avec les plantes","croissance végétale","dissipation de la magie","état cadavérique","fusion dans la pierre","invocation d'animaux","lumière du jour","marche sur l'onde","mur de vent","protection contre l'énergie","respiration aquatique","tempête de neige"],
            ["confusion","contrôle de l'eau","domination d'animal","façonnage de la pierre","flétrissement","insecte géant","invocation d'élémentaires mineurs","invocation d'êtres sylvestres","liane avide","liberté de mouvement","localisation de créature","métamorphose","mur de feu","peau de pierre","tempête de grêle","terrain hallucinatoire"],
            ["communion avec la nature","contagion","coquille antivie","entrave planaire","éveil","fléau d'insectes","invocation d'élémentaire","mur de pierre","passage par les arbres","quête","réincarnation","restauration suprême","scrutation","soins de groupe"],
            ["festin des héros","glissement de terrain","guérison","invocation de fée","mur d'épines","orientation","rayon de soleil","vent divin","voie végétale"],
            ["changement de plan","inversion de la gravité","mirage","régénération","tempête de feu"],
            ["aversion/attirance","contrôle du climat","éclat du soleil","esprit faible","métamorphose animale","tremblement de terre","tsunami"],
            ["changement de forme","prémonition","résurrection suprême","tempête vengeresse"]],
        "ensorceleur" : [
            ["aspersion acide","bouffée de poison","contact glacial","coup au but","faux amis illusion mineure","lumière","lumières dansantes","main du mage","message","poigne électrique","prestidigitation","protection contre les armes","rayon de givre","réparation","trait de feu"],
            ["armure du mage","bouclier","charme-personne","compréhension des langues","couleurs dansantes","déguisement","détection de la magie","feuille morte","image silencieuse","mains brûlantes","nappe de brouillard","orbe chromatique","projectile magique","rayon empoisonné","repli expéditif","saut","simulacre de vie","sommeil","trait ensorcelé","vague tonnante"],
            ["agrandissement/rapetissement","amélioration de caractéristique","bourrasque","cécité/surdité","couronne du dément","déblocage","détection de l'invisibilité","détection des pensées","flou","force fantasmagorique","foulée brumeuse","fracassement","image miroir","immobilisation de personne","invisibilité","lévitation","modification d'apparence","nuée de dagues","pattes d'araignée","rayon ardent","suggestion","ténèbres","toile d'araignée","vision dans le noir"],
            ["boule de feu","clairvoyance","clignotement","contresort","dissipation de la magie","don des langues","éclair","forme gazeuse","hâte","image majeure","lenteur","lumière du jour","marche sur l'onde","motif hypnotique","nuage nauséabond","protection contre l'énergie","respiration aquatique","tempête de neige","terreur","vol"],
            ["bannissement","confusion","domination d'animal","flétrissement","invisibilité suprême","métamorphose","mur de feu","peau de pierre","porte dimensionnelle","tempête de grêle"],
            ["animation des objets","apparence trompeuse","brume mortelle","cercle de téléportation","cône de froid","création","domination de personne","fléau d'insectes","immobilisation de monstre","mur de pierre","télékinésie"],
            ["cercle de mort","chaîne d'éclairs","désintégration","glissement de terrain","globe d'invulnérabilité","mauvais œil","portail arcanique","rayon de soleil","suggestion de groupe","vision suprême"],
            ["boule de feu à retardement","changement de plan","doigt de mort","embruns prismatiques","forme éthérée","inversion de la gravité","téléportation","tempête de feu"],
            ["domination de monstre","éclat du soleil","mot de pouvoir étourdissant","nuage incendiaire","tremblement de terre"],
            ["arrêt du temps","mot de pouvoir mortel","nuée de météores","portail","souhait"]],
        "magicien" : [
            ["aspersion acide","bouffée de poison","contact glacial","coup au but","faux amis","illusion mineure","lumière","lumières dansantes","main du mage","message","poigne électrique","prestidigitation","protection contre les armes","rayon de givre","réparation","trait de feu"],
            ["alarme","appel de familier","armure du mage","bouclier","charme-personne","compréhension des langues","couleurs dansantes","déguisement","détection de la magie","disque flottant de Tenser","feuille morte","fou rire de Tasha","graisse","grande foulée","identification","image silencieuse","mains brûlantes","nappe de brouillard","orbe chromatique","projectile magique","protection contre le mal et le bien","rayon empoisonné","repli expéditif","saut","serviteur invisible","simulacre de vie","sommeil","texte illusoire","trait ensorcelé","vague tonnante"],
            ["agrandissement/rapetissement","arme magique","aura magique de Nystul","bouche magique","bourrasque","cécité/surdité","corde enchantée","couronne du dément","déblocage","détection de l'invisibilité","détection des pensées","doux repos","flamme éternelle","flèche acide de Melf","flou","force fantasmagorique","foulée brumeuse","fracassement","image miroir","immobilisation de personne","invisibilité","lévitation","localisation d'objet","modification d'apparence","nuée de dagues","pattes d'araignée","rayon affaiblissant","rayon ardent","sphère de feu","suggestion","ténèbres","toile d'araignée","verrou magique","vision dans le noir"],
            ["animation des morts","antidétection","boule de feu","caresse du vampire","cercle magique","clairvoyance","clignotement","communication à distance","contresort","délivrance des malédictions","dissipation de la magie","don des langues","éclair","état cadavérique","forme gazeuse","glyphe de garde","hâte","image majeure","lenteur","malédiction","monture fantôme","motif hypnotique","nuage nauséabond","petite hutte de Léomund","protection contre l'énergie","respiration aquatique","tempête de neige","terreur","vol"],
            ["assassin imaginaire","bannissement","bouclier de feu","chien de garde de Mordenkainen","coffre secret de Léomund","confusion","contrôle de l'eau","fabrication","façonnage de la pierre","flétrissement","invisibilité suprême","invocation d'élémentaires mineurs","localisation de créature","métamorphose","mur de feu","œil du mage","peau de pierre","porte dimensionnelle","sanctuaire privé de Mordenkainen","sphère résiliente d'Otiluke","tempête de grêle","tentacules noirs d'Evard","terrain hallucinatoire"],
            ["animation des objets","apparence trompeuse","brume mortelle","cercle de téléportation","cône de froid","contact avec les plans","création","domination de personne","double illusoire","entrave planaire","immobilisation de monstre","invocation d'élémentaire","lien télépathique de Rary","main de Bigby","modification de mémoire","mur de force","mur de pierre","mythes et légendes","passe-muraille","quête","scrutation","songe","télékinésie"],
            ["anticipation","cercle de mort","chaîne d'éclairs","convocations instantanées de Drawmij","création de mort-vivant","danse irrésistible d'Otto","désintégration","glissement de terrain","globe d'invulnérabilité","illusion programmée","mauvais œil","mur de glace","pétrification","portail arcanique","possession","protections et sceaux","rayon de soleil","sphère glacée d'Otiluke","suggestion de groupe","vision suprême"],
            ["boule de feu à retardement","cage de force","changement de plan","dissimulation suprême","doigt de mort","embruns prismatiques","épée de Mordenkainen","forme éthérée","image projetée","inversion de la gravité","manoir somptueux de Mordenkainen","mirage","simulacre","symbole","téléportation"],
            ["aversion/attirance","champ antimagie","clone","contrôle du climat","dédale","demi-plan","domination de monstre","éclat du soleil","esprit faible","esprit impénétrable","mot de pouvoir étourdissant","nuage incendiaire","télépathie"],
            ["arrêt du temps","changement de forme","emprisonnement","ennemi subconscient","métamorphose suprême","mot de pouvoir mortel","mur prismatique","nuée de météores","portail","prémonition","projection astrale","souhait"]],
        "occultiste" : [
            ["bouffée de poison","contact glacial","coup au but","décharge occulte","faux amis","illusion mineure","main du mage","prestidigitation","protection contre les armes"],
            ["armure d'Agathys","charme-personne","compréhension des langues","maléfice","protection contre le mal et le bien","repli expéditif","représailles infernales","serviteur invisible","tentacules de Hadar","texte illusoire","trait ensorcelé"],
            ["couronne du dément","discours captivant","foulée brumeuse","fracassement","image miroir","immobilisation de personne","invisibilité","nuée de dagues","pattes d'araignée","rayon affaiblissant","suggestion","ténèbres"],
            ["caresse du vampire","cercle magique","contresort","délivrance des malédictions","dissipation de la magie","don des langues","forme gazeuse","image majeure","motif hypnotique","terreur","vol","voracité de Hadar"],
            ["bannissement","flétrissement","porte dimensionnelle","terrain hallucinatoire"],
            ["contact avec les plans","immobilisation de monstre","scrutation","songe"],
            ["cercle de mort","création de mort-vivant","invocation de fée","mauvais œil","pétrification","portail arcanique","suggestion de groupe","vision suprême"],
            ["cage de force","changement de plan","doigt de mort","forme éthérée"],
            ["bagou","demi-plan","domination de monstre","esprit faible","mot de pouvoir étourdissant"],
            ["emprisonnement","métamorphose suprême","mot de pouvoir mortel","prémonition","projection astrale"]],
        "paladin" : [
            [],
            ["bénédiction","bouclier de la foi","châtiment calcinant","châtiment courroucé","châtiment tonitruant","détection de la magie","détection du mal et du bien","détection du poison et des maladies","duel forcé","faveur divine","héroïsme","injonction","protection contre le mal et le bien","purification de la nourriture et de l'eau","soins"],
            ["aide","appel de destrier","arme magique","châtiment révélateur","localisation d'objet","protection contre le poison","restauration partielle","zone de vérité"],
            ["arme élémentaire","aura de vitalité","aura du croisé","cercle magique","châtiment aveuglant","création de nourriture et d'eau","délivrance des malédictions","dissipation de la magie","lumière du jour","retour à la vie"],
            ["aura de pureté","aura de vie","bannissement","châtiment débilitant","localisation de créature","protection contre la mort"],
            ["cercle de pouvoir","châtiment du ban","dissipation du mal et du bien","quête","rappel à la vie","vague destructrice"],
            [],[],[],[]],
        "rodeur" : [
            [],
            ["alarme","amitié avec les animaux","baies nourricières","communication avec les animaux","détection de la magie","détection du poison et des maladies","frappe piégeuse","grande foulée","grêle d'épines","marque du chasseur","nappe de brouillard","saut","soins"],
            ["cordon de flèches","croissance d'épines","détection des pièges","localisation d'animaux ou de plantes","localisation d'objet","messager animal","passage sans trace","peau d'écorce","protection contre le poison","restauration partielle","sens animal","silence","vision dans le noir"],
            ["antidétection","communication avec les plantes","croissance végétale","flèche de foudre","hérissement de projectiles","invocation d'animaux","lumière du jour","marche sur l'onde","mur de vent","protection contre l'énergie","respiration aquatique"],
            ["invocation d'êtres sylvestres","liane avide","liberté de mouvement","localisation de créature","peau de pierre"],
            ["communion avec la nature","invocation de volée","passage par les arbres","vif carquois"],
            [],[],[],[],[]]}
    page = exctaction_nom_sort_all()
    spells = []#Création d'une liste
    for row in soup.find_all('tr')[1:]:  # Pour chaque ligne de sort
        cols = row.find_all('td') #Permet de récupérer chaque collone de la ligne correspondante

        source = cols[12].text.strip() #Récupère la source du sort (Soit Player of Handbook, soit Xanathar´s Guide to Everything, soit Tasha´s Cauldron of Everything)
        name = cols[1].text.strip() #Récupère le nom du sort
        level = cols[4].text.strip() #Récupère le niveaux du sort

        if source in ["Player´s Handbook (SRD)", "Player´s Handbook (BR+)", "Player´s Handbook"]: #Si la source du sort est le Player of Handbook
            spell = { #Création d'un dictionnaire
                'name': name, #Nom du sort
                'level': level, #Niveaux du sort
                'school': cols[5].text.strip(), #Ecole du sort
                'casting_time': cols[6].text.strip(), #Incantation
                'range': cols[7].text.strip(), #Portée
                'components': cols[8].text.strip(), #V, S, M
                'concentration': "Concentration" == cols[9].text.strip(), #Concentration True/False
                'rituel': "Rituel" == cols[10].text.strip(), #Rituel True/False
                'description': cols[11].text.strip(), #Description
                'barde': recuperation_page_classe(page, sort_classe, level, name, "barde"),
                'clerc': recuperation_page_classe(page, sort_classe, level, name, "clerc"),
                'druide': recuperation_page_classe(page, sort_classe, level, name, "druide"),
                'ensorceleur': recuperation_page_classe(page, sort_classe, level, name, "ensorceleur"),
                'magicien': recuperation_page_classe(page, sort_classe, level, name, "magicien"),
                'paladin': recuperation_page_classe(page, sort_classe, level, name, "paladin"),
                'occultiste': recuperation_page_classe(page, sort_classe, level, name, "occultiste"),
                'rodeur': recuperation_page_classe(page, sort_classe, level, name, "rodeur"),
                
                #Page dans le pdf de tous les sorts
                'multiclasse' : recuperation_page_classe(page, sort_classe, level, name, "multiclasse")
            }
            

            spells.append(spell) #Ajout du dictionaire

    with open(recuper_chemin_absolue + '/data/spells.json', 'w', encoding='utf-8') as f: #Ouverture/Création du fichier json "spells.json"
        json.dump(spells, f, ensure_ascii=False, indent=4) #Ajout/Modification des sorts

#scrapping_sort()