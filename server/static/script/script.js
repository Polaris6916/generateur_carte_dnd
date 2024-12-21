//Varirable global
let sort_json = [];
var classe_selectionner = "multiclasse";
let selectedRows = [];

//Fonction qui permet d'afficher qu'elle carte est sélectionner
function card_selection(classe){    
    var element = document.getElementById('card_'+ classe_selectionner); //On récupère la carte actuellement sélectionner
    element.style.display = "none"; //On fait disparaitre la bulle au-dessus d'elle

    classe_selectionner = classe; //On définis la nouvelle classe sélectionné
    var element = document.getElementById('card_'+ classe_selectionner); //On récupère sont id
    element.style.display = "block"; //On affiche l'indicateur 

}

//Fonction pour le tableau
async function tableau_selector(classe) {
    card_selection(classe); // Permet de modifier la petite icône au-dessus de la carte sélectionnée
    selectedRows = []; //Permet d'enlever les éléments checker

    // Si le tableau n'est pas initialisé, initialiser
    if (!$('#table_bootstrap').hasClass('initialized')) {
        $('#table_bootstrap').bootstrapTable({
            pagination: true,                // Activer la pagination
            paginationVAlign: 'both',        // Aligner la pagination en haut et en bas
            pageSize: 20,                    // Taille de page (nombre de lignes par page)
            pageList: [10, 20, 50, 100, 200, "All"],
            sortable: true,                  // Activer le tri
            columns: [{
                field: 'state',
                checkbox: true,              // Champ pour la case à cocher
                formatter: (value, row, index) => {
                    // Si la ligne est dans la liste des éléments sélectionnés, cochez la case
                    return selectedRows.includes(row.id) ? { checked: true } : { checked: false };
                }
            }, {
                field: 'name',               // Nom de la colonne
                visible: true                // Rendre cette colonne visible
            }, {
                field: 'level',
                visible: true                 // Rendre cette colonne visible
            }, {
                field: 'school',
                visible: true                 // Rendre cette colonne visible
            }, {
                field: 'casting_time',
                visible: false,                // Masquer cette colonne par défaut
                sortable: true,
                sorter: (a, b) => {          // Fonction de tri personnalisée
                    const getRank = (value) => {
                        if (value === "1 réaction") return 1;
                        if (value === "1 action bonus") return 2;
                        if (value === "1 action") return 3;
                        if (value === "1 action ou 8 heures") return 4;
                        if (value === "1 minute") return 5;
                        if (/\d+\s?minutes$/.test(value)) return 6;
                        if (value === "1 heure") return 7;
                        if (/\d+\s?heures$/.test(value)) return 8;
                        return 9; // Valeur par défaut pour les autres
                    };

                    const extractNumber = (value) => {
                        const match = value.match(/(\d+\.\d+|\d+)\s?(minutes|heures)?/);  // Capture le nombre (entier ou flottant), puis "m" ou "km"
                        return match ? parseFloat(match[1]) : 0;   // Retourne le nombre (en tant que flottant)
                    };

                    const rankA = getRank(a);
                    const rankB = getRank(b);

                    if (rankA == rankB){
                        if (rankA == 5)
                        {
                            if (extractNumber(a) - extractNumber(b) > 0)
                                {
                                    return 1;
                                }
                                else
                                {
                                    return -1;
                                }
                        }
                        else {
                            if (rankA == 7) {
                                if (extractNumber(a) - extractNumber(b) > 0)
                                    {
                                        return 1;
                                    }
                                    else
                                    {
                                        return -1;
                                    }
                            }
                            else
                            {
                                return 0;
                            }
                        }
                    }
                    else {
                        return rankA-rankB;
                    }
                }
            }, {
                field: 'range',
                visible: true,                // Rendre cette colonne visible
                sortable: true,
                sorter: (a, b) => {          // Fonction de tri personnalisée pour la colonne "range"
                    const getRank = (value) => {
                        if (value === 'perso') return 0;
                        if (/^perso\w*/.test(value)) return 1; // "perso" suivi de texte
                        if (value === 'contact') return 2;
                        if (value === 'champ de vision') return 3;
                        if (/\d+\s?km$/.test(value)) return 5;   // Nombre suivi de "km"
                        if (/\d+\s?m$/.test(value)) return 4;    // Nombre suivi de "m"
                        if (value === 'illimitée') return 6;
                        if (value === 'spécial') return 7;
                        return 8;                           // Valeur par défaut pour les autres
                    };

                    const extractNumber = (value) => {
                        const match = value.match(/(\d+\.\d+|\d+)\s?(m|km)?/);  // Capture le nombre (entier ou flottant), puis "m" ou "km"
                        return match ? parseFloat(match[1]) : 0;   // Retourne le nombre (en tant que flottant)
                    };

                    const rankA = getRank(a);
                    const rankB = getRank(b);

                    if (rankA === rankB) {
                        if (rankA === 1) {
                            return a.localeCompare(b);
                        } else {
                            if (rankA === 3)
                            {
                                if (extractNumber(a) - extractNumber(b) > 0)
                                {
                                    return 1;
                                }
                                else
                                {
                                    return -1;
                                }
                            }
                            else
                            {
                                if (rankA === 4)
                                {
                                    if (extractNumber(a) - extractNumber(b) > 0)
                                        {
                                            return 1;
                                        }
                                        else
                                        {
                                            return -1;
                                        }
                                }
                                else
                                {
                                    return 0;  // Si les rangs sont égaux, on ne change rien (car ils sont déjà égaux)
                                }
                            }
                        }
                    } else {
                        return rankA - rankB;
                    }
                }
            }, {
                field: 'components',
                visible: true,                 // Rendre cette colonne visible
                sortable: true,
                sorter: (a, b) => {
                    const getRank = (value) => {
                        if (value == "V") return 1;
                        if (value == "S") return 2;
                        if (value == "M") return 3;
                        if (value == "V,S") return 4;
                        if (value == "V,M") return 5;
                        if (value == "S,M") return 6;
                        if (value == "V,S,M") return 7;
                        return 8;
                    }
                    return getRank(a)-getRank(b);
                }
            }, {
                field: 'concentration',
                visible: false,               // Masquer cette colonne par défaut
                sortable: true,
                sorter: (a, b) => {
                    const getRank = (value) => {
                        if (value == "Oui") return 1;
                        if (value == "Non") return 2;
                        return 3;
                    }
                    return getRank(a)-getRank(b);
                }
            }, {
                field: 'rituel',
                visible: false,                // Masquer cette colonne par défaut
                sortable: true,
                sorter: (a, b) => {
                    const getRank = (value) => {
                        if (value == "Oui") return 1;
                        if (value == "Non") return 2;
                        return 3;
                    }
                    return getRank(a)-getRank(b);
                }
            }, {
                field: 'description',
                visible: false                // Masquer cette colonne par défaut
            }, {
                field: 'page',                // Colonne "Page" (cachée)
                visible: false,               // Toujours masquée
                switchable: false,            // Ne pas jamais être affichée
                title: 'Page'
            }],
            showColumns: true,                // Afficher le bouton pour sélectionner les colonnes
            showColumnsToggleAll: true,       // Afficher le bouton pour sélectionner/désélectionner toutes les colonnes sauf "Page"
            checkboxHeader: true,             // Ajouter la case à cocher "Sélectionner tout"
            clickToSelect: false,             // Ne pas sélectionner les lignes en cliquant sur une cellule
            locale: 'fr-FR',                  // Permet d'avoir les interface de bootstrap table en français
            loadingFontSize: true,            // Permet d'avoir un écran de chargement (non utilisée)
            onCheckAll: (rows) => {           // Lorsque on active le bouton qui permet de checker la page entière alors aplique la fonction
                rows.forEach(row => {         // Boucle pour prendre toute les lignes de la page
                    if (!selectedRows.includes(row.id)) { //Si l'ID n'est pas déjà dans la liste slectedRows
                        selectedRows.push(row.id); // Alros ajout l'ID de la ligne sélectionnée
                    }
                });
            },
            onUncheckAll: () => { //Fonction lorsque on décheck le bouton check all du tableaux
                // Récupérer toutes les lignes actuellement affichées dans le tableau
                const visibleRows = $('#table_bootstrap').bootstrapTable('getData', { useCurrentPage: true });
                                        
                visibleRows.forEach(row => {
                    // Retirer uniquement les IDs des lignes affichées de la liste selectedRows
                    selectedRows = selectedRows.filter(id => id !== row.id);
                });
            },
            onCheck: (row) => { //Lors d'un check d'une ligne
                selectedRows.push(row.id); // Ajouter l'ID de la ligne sélectionnée
            },
            onUncheck: (row) => { //Lors d'un décheck d'une ligne
                selectedRows = selectedRows.filter(id => id !== row.id); // Retirer l'ID de la ligne décochée
            }
        });
        $('#table_bootstrap').addClass('initialized'); // Pour initialiser le tableaux
    }

    const url = "spells.html/" + classe; //Construction de l'url
    const response = await fetch(url); //On envoie la réponse au server
    const donneesCompletes = await response.json(); //On déchiffre le paquet envoyer en un fichier json

    // Transformation des données pour inclure uniquement la colonne "Page" liée à la classe donnée
    const donneesFiltrees = donneesCompletes.map((sort, index) => ({
        id: index,                                          // Utiliser l'index comme ID unique
        name: sort.name,                                    //Nom du sort
        level: sort.level,                                  //Level du sort
        school: sort.school,                                //Ecole du sort
        casting_time: sort.casting_time,                    //Temps pour lancer le sort
        range: sort.range,                                  //Portée du sort
        components: sort.components,                        //Composant du sort (matériel, visuel ou/et somatique)
        concentration: sort.concentration ? "Oui" : "Non",  //Suivant la valeur true/false affiche Oui ou Non pour la concentration
        rituel: sort.rituel ? "Oui" : "Non",                //Suivant la valeur true/false affiche Oui ou Non pour le rituel
        description: sort.description,                      //Description du sort
        page: sort[classe]?.[1]?.join("-") || "-"           // Récupère les niveaux pour la classe ou affiche "-" si vide (jamais affiché)
    }));

    $('#table_bootstrap').bootstrapTable('load', donneesFiltrees); //Permet d'afficher les lignes de la liste donnesFiltrées
}

//Fonction qui permet de s'avoir qu'elle page est sélectionner
function getSelectedPages() {
    // Récupère toutes les lignes de la table
    const allRows = $('#table_bootstrap').bootstrapTable('getData');
    
    // Crée une nouvelle liste avec les lignes correspondant aux indices de selectedRows
    const selectedData = selectedRows.map(id => allRows.find(row => row.id === id));
    const pages = selectedData
        .map(row => row.page) // Récupère la valeur de la colonne "Page"
        .join("-"); // Concatène les pages avec un tiret

    return pages ? `-${pages}` : ""; // Ajoute un tiret au début uniquement s'il y a des données
}

//Function qui permet de checker tous les sorts de toute les lignes
function checkAllRows() {
    // Récupérer toutes les données du tableau
    const allRows = $('#table_bootstrap').bootstrapTable('getData');
    
    // Ajouter tous les IDs à la liste `selectedRows` (éviter les doublons)
    selectedRows = allRows.map(row => row.id);

    // Activer toutes les cases cochées directement dans les données du tableau
    allRows.forEach(row => {
        row.state = true; // Définit l'état de chaque ligne à "coché"
    });

    // Recharger les données avec les cases cochées
    $('#table_bootstrap').bootstrapTable('load', allRows);
}

//Fonction qui permet de déchecker toute les lignes du tableaux
function uncheckAllRows() {
    // Réinitialiser la liste des lignes sélectionnées
    selectedRows = [];

    // Récupérer toutes les données du tableau
    const allRows = $('#table_bootstrap').bootstrapTable('getData');

    // Mettre à jour toutes les lignes pour décocher les cases
    allRows.forEach(row => {
        row.state = false; // Définit l'état de chaque ligne à "non coché"
    });

    // Recharger les données dans le tableau avec les lignes décochées
    $('#table_bootstrap').bootstrapTable('load', allRows);
}

//Fonction pour générer le pdf
async function generer_pdf() {
    const page = getSelectedPages(); //Permet de récupré le txt de toute les sort sélectionner
    const div_aler = document.getElementById("aucune_selection");

    if (page != "") { //Si il y a des sorts sélectionner
        var url = "pdf.html/" + classe_selectionner + "/" + page; //Construction du l'url

        try { //Esseye de faire la requete pour la constrcution du pdf
            document.getElementById("spinner_pdf").style.display = "block"; //Permet d'afficher le loader

            const response = await fetch(url); //Envoie de la requete
            if (!response.ok) { //Si la requête n'est pas of
                throw new Error('Network response was not ok');
            }

            //Téléchargement et envoie du fichier pdf
            const blob = await response.blob();
            const urlBlob = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = urlBlob;
            a.download = 'carte_genener.pdf'; // Nom du fichier à télécharger
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(urlBlob);

            document.getElementById("spinner_pdf").style.display = "none"; //Enlève le loader

        } catch (error) {
            console.error('There was a problem with the fetch operation:', error);
        }
    }
    else {
        window.showToast(); //Affiche le toast si il n'y a pas de sort sélectionner
    }
}

//Fonction pour le loader
document.addEventListener('DOMContentLoaded', function () { //Déclare la fonction après que tout le contenue soit chargé (mais avant les images)
    // Fonction pour afficher le toast
    function showToast() {
        const toastElement = document.getElementById('liveToast');
        if (toastElement) {
            const toast = bootstrap.Toast.getOrCreateInstance(toastElement);
            toast.show();  // Affiche le toast
        } else {
            console.error('Toast element not found!');
        }
    }

    // Assurez-vous que la fonction est accessible globalement
    window.showToast = showToast;

    // Écouteur d'événement pour le bouton
    const toastTrigger = document.getElementById('liveToastBtn');
    if (toastTrigger) {
        toastTrigger.addEventListener('click', showToast);
    } else {
        console.error('Toast button not found!');
    }
});


//Après que toute la page soit loader appelle la fonction pour construire le tableaux
window.onload = function(){
    tableau_selector('multiclasse');
}