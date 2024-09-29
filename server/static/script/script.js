let sort_json = [];

//Fonction permettant de appliqué le critère de tris de l'utilisateur
function display_tableaux(type) { 
    // Récupère l'état de la case à cocher associée au type donné
    const check_box = document.getElementById("check_" + type).checked;

    // Convertit la collection HTML des éléments avec la classe spécifiée en un tableau
    const display_element_array = Array.from(document.getElementsByClassName(type));

    // Parcourt chaque élément du tableau
    display_element_array.forEach(element => {
        // Si la case à cocher est cochée, affiche l'élément en tant que cellule de tableau
        if (check_box) {
            element.style.display = "table-cell";
        } else { // Sinon, cache l'élément
            element.style.display = "none";
        }
    });
}

//Fonction qui permet de cocher ou décocher toute les case
function check_all (){
    const check_box = document.getElementById("check_all").checked; //Constante bool pour voir sur check_all est checher ou pas
    var index = 0;

    const display_element_array = Array.from(document.getElementsByName("check_sort")); //Liste qui a tous les éléments de check sort

    if (check_box){ //Si la box check_all est checker alors
        display_element_array.forEach(element =>{ //Pour chaque élément
            index++;
            document.getElementById("check_"+index).checked = true; // On met la valeur checked
        })
    }
    else{ //Sinon
        display_element_array.forEach(element =>{
            index++;
            document.getElementById("check_"+index).checked = false; //On enlève pour tous la valeur checker
        })
    }
}

//Fonction qui permet de triée les éléments selon la demande de l'utilisateur
function trie(type){
    document.getElementById("type_trie").value = type; //Modifie le type de trie voulue
    sort_tableaux(); //Appelle la fonction qui permet de trier
}

//Fonction qui permet de supprimer toute les ligne du tableaux de sort sauf la 1er
function supprimer_liste_sort(){ 
    const table = document.getElementById("tableau_sort"); //Récupère le tableau
    const longeur_table = table.rows.length; //Récupère le nombre de ligne de se tableau

    for (let ligne = 1; ligne < longeur_table; ligne++){ //Boucle pour supprimer chaque ligne de se tableaux
        table.deleteRow(1); //Suprime la 2e ligne (soit la 1er car commence à partir de 0)
    }
}

//Fonction utiliser pour savoir si un sort est un rituel/concentration ou pas
function type_true_false(reponse){
    if (reponse){ //la réponse est en boolléen si oui
        return "Oui" //Renvoie oui
    }
    else {
        return "" //Sinon renvoie une chaine de caractère vide
    }
}

//Fonction qui permet de rendre une liste en texte pour savoir où sont les pages
function page(reponse){
    //Déclaration de variable
    var liste_numeros = "";
    
    reponse.forEach(numero =>{ //Pour chaque élément de la liste
        liste_numeros = liste_numeros + "-" + numero; //rajoute l'autre numero
    })
    return liste_numeros; //Retourne la liste complet
}

//Fonction qui permet de savoir qu'elle pour quelle trie on est
function page_trie(sort, classe){
    if (classe=="multiclasse"){ //Si la classe du sort selectionner est multiclasse
        return page(sort.multiclasse[1]); //retourne en appellant la fonction page
    }
    else if (classe=="barde"){ //Si la classe du sort selectionner est
        return page(sort.barde[1]); //retourne en appellant la fonction page
    }
    else if (classe=="clerc"){ //Si la classe du sort selectionner est clerc
        return page(sort.clerc[1]); //retourne en appellant la fonction page
    }
    else if (classe=="druide"){ //Si la classe du sort selectionner est druide
        return page(sort.druide[1]); //retourne en appellant la fonction page
    }
    else if (classe=="ensorceleur"){ //Si la classe du sort selectionner est ensorceleur
        return page(sort.ensorceleur[1]); //retourne en appellant la fonction page
    }
    else if (classe=="magicien"){ //Si la classe du sort selectionner est magicien
        return page(sort.magicien[1]); //retourne en appellant la fonction page
    }
    else if (classe=="occultiste"){ //Si la classe du sort selectionner est occultiste
        return page(sort.occultiste[1]); //retourne en appellant la fonction page
    }
    else if (classe=="paladin"){ //Si la classe du sort selectionner est paladin
        return page(sort.paladin[1]); //retourne en appellant la fonction page
    }
    else if (classe=="rodeur"){ //Si la classe du sort selectionner est rodeur
        return page(sort.rodeur[1]); //retourne en appellant la fonction page
    }
    
}

//Fonction qui permet de trier la liste en entrée selon le type (ex: par le nom, niveaux..)
function trie_liste_sort(type, liste){ 
    if (type == "nom") { //Si le type selectionner est nom
        liste.sort((a,b)=> { //Boucle qui reprend tous les sort
            if (a.name < b.name) return -1; //Si b est avant a alors b passe devant
            if (a.nom > b.nom) return 1; //Si a est avant b alors a passe devant
            return 0; //Sinon rien ne se passe
        })
    }
    else if (type == "niveau"){ //Si le type selectionner est niveaux
        liste = trie_liste_sort("nom", liste); //Permet de d'abord triés par nom
        liste.sort((a, b) => a.level - b.level); //reprend les sorts et les trie selon leur niveaux
    }
    else if (type == "ecole"){ 
        liste = trie_liste_sort("nom", liste);
        liste.sort((a,b)=> { //Boucle qui reprend tous les sort
            if (a.school < b.school) return -1; //Si b est avant a alors b passe devant
            if (a.school > b.school) return 1; //Si a est avant b alors a passe devant
            return 0;
        })
    }
    else if (type == "incantation"){ //Si le type selectionner est  incantation
        liste = trie_liste_sort("nom", liste); //Permet de d'abord triés par nom
        liste.sort((a,b)=> { //Boucle qui reprend tous les sort
            if (a.casting_time < b.casting_time) return -1; //Si b est avant a alors b passe devant
            if (a.casting_time > b.casting_time) return 1; //Si a est avant b alors a passe devant
            return 0;
        })
    }
    else if (type == "portee"){ //Si le type selectionner est portée
        liste = trie_liste_sort("nom", liste); //Permet de d'abord triés par nom
        liste.sort((a,b)=> { //Boucle qui reprend tous les sort
            if (a.range < b.range) return -1; //Si b est avant a alors b passe devant
            if (a.range > b.range) return 1; //Si a est avant b alors a passe devant
            return 0;
        })
    }
    else if (type == "vsm"){ //Si le type selectionner est les composent
        liste = trie_liste_sort("nom", liste); //Permet de d'abord triés par nom
        liste.sort((a,b)=> { //Boucle qui reprend tous les sort
            if (a.components < b.components) return -1; //Si b est avant a alors b passe devant
            if (a.components > b.components) return 1; //Si a est avant b alors a passe devant
            return 0;
        })
    }
    else if (type == "concentration"){ //Si le type selectionner est concentration
        liste = trie_liste_sort("nom", liste); //Permet de d'abord triés par nom
        liste.sort((a,b)=> { //Boucle qui reprend tous les sort
            if (a.concentration < b.concentration) return 1; //Si a est avant b alors a passe devant
            if (a.concentration > b.concentration) return -1; //Si b est avant a alors b passe devant
            return 0;
        })
    }
    else if (type == "rituel"){ //Si le type selectionner est rituel
        liste = trie_liste_sort("nom", liste); //Permet de d'abord triés par nom
        liste.sort((a,b)=> { //Boucle qui reprend tous les sort
            if (a.rituel < b.rituel) return 1; //Si a est avant b alors a passe devant
            if (a.rituel > b.rituel) return -1; //Si b est avant a alors b passe devant
            return 0;
        })
    }
    else if (type == "description"){ //Si le type selectionner est description
        liste = trie_liste_sort("nom", liste); //Permet de d'abord triés par nom
        liste.sort((a,b)=> { //Boucle qui reprend tous les sort
            if (a.description < b.description) return -1; //Si b est avant a alors b passe devant
            if (a.description > b.description) return 1; //Si a est avant b alors a passe devant
            return 0;
        })
    }
    return liste;
}

//Permet de voir combien on a de niveaux
function niveaux(){
    valeur_min = document.getElementById("niveaux_min").value;
    valeur_max = document.getElementById("niveaux_max").value;
    if (valeur_min >= valeur_max) {
        valeur_max = document.getElementById("niveaux_max").value = valeur_min;
    }
}

//Fonction qui permet de remplir le tableaux selon la classe de sort séléctionner ainsi que le trie que l'on demande
function sort_tableaux(){
    let liste_sort = sort_json;

    const table = document.getElementById("tableau_sort"); //Récupère le tableux
    var index = 0; //Permet de garder le nombre de ligne que l'on a

    const type_trie = document.getElementById("type_trie").value;
    supprimer_liste_sort();//Permet de supprimer les sort restants
    niveaux(); //Permet de rectifier les niveaux au besoins

    liste_sort = trie_liste_sort(type_trie, liste_sort);
    liste_sort.forEach(sort => { //Boucle pour remplir le tableux
        const niveau = sort.level;
        if (document.getElementById('niveaux_min').value <= niveau && document.getElementById('niveaux_max').value >= niveau){
            index++; //Incrementation de index
            var newRow = table.insertRow(index) //Variable de création d'une ligne vide
    
            var contenue_ligne = '<tr>' //Contenue de la ligne
                    + '<th scope="row">'
                    +   '<div class="form-check">'
                    +   '<input class="form-check-input" name="check_sort" type="checkbox" value="" id="check_'+ index +'">'
                    +   '<label class="form-check-label" for="flexCheckDefault">'
                    +   '</label>'
                    + '</div></th>'
                    + '<td>'+ sort.name +'</td>'
                    + '<td>'+ niveau +'</td>'
                    + '<td class="ecole">'+ sort.school +'</td>'
                    + '<td class="incantation">'+ sort.casting_time +'</td>'
                    + '<td class="portee">'+ sort.range+'</td>'
                    + '<td class="vsm">'+ sort.components +'</td>'
                    + '<td class="concentration">'+ type_true_false(sort.concentration) +'</td>'
                    + '<td class="rituel">'+ type_true_false(sort.rituel) +'</td>'
                    + '<td class="description">'+ sort.description +'</td>'
                    + '<td class="page" id="page_'+index+'">'+ page_trie(sort, document.getElementById("type_classe").value) +'</td>'
                    + '</tr>';
            newRow.innerHTML = contenue_ligne; //Ajoute se contenue dans la ligne vide 
        }
    })

    //Permet de mettre à jour les critères de selection choisie par l'utilisateur
    let liste_type_display = ['ecole', 'incantation', 'portee', 'vsm', 'concentration','rituel', 'description'];
    liste_type_display.forEach(type_element => {
        display_tableaux(type_element);
    })

    document.getElementById("check_all").checked = false; //Permet désactiver le check global
}

//Permet de renvoyer toute les pages où les sort sont checher
function liste_check_sort(){
    var index = 0;
    const display_element_array = Array.from(document.getElementsByName("check_sort")); //Liste qui a tous les éléments de check sort
    let liste_page_checker = ""

    display_element_array.forEach(element =>{ //Pour chaque élément
        index++;
        if (element.checked) {
            liste_page_checker = liste_page_checker + document.getElementById('page_'+index).textContent;
        }
    })
    return liste_page_checker
}

//Fonction pour récuperer la liste de sort
async function tableau_selector(classe) { 
    supprimer_liste_sort(); //Supprime les sorts présent
    var url="spells.html/"+classe; //Construction de l'url pour demander le fichier json

    const response = await fetch(url); //Envoie de la requête et attend la réponse
    var liste_sort = await response.json(); //Extrait le json de la réponse
    
    sort_json = liste_sort;
    document.getElementById("type_classe").value = classe
    sort_tableaux();
}

//Fonction pour générer le pdf
async function generer_pdf() {
    const page = liste_check_sort();
    const div_aler = document.getElementById("aucune_selection");

    if (page != "") {
        var url = "pdf.html/" + document.getElementById("type_classe").value + "/" + page;

        try {
            const response = await fetch(url);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            const blob = await response.blob();
            const urlBlob = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = urlBlob;
            a.download = 'carte_genener.pdf'; // Nom du fichier à télécharger
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(urlBlob);
        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }
    else {
        alert("Tu n'as pas sélectionner de sort. Je ne peux pas créer tes cartes");
    }
}


//Au chargement de la page permet de mettre tout les sorts
window.onload = function(){
    tableau_selector('multiclasse');
}