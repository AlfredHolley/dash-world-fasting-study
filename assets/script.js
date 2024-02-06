function updateDivDisplay(n_click_timestamp) {
    var divElement = document.getElementById('X-heatmap-div');
    
    if (n_click_timestamp === null) {
        // Gérer le cas où n_click_timestamp est null (premier chargement de la page ou valeur manquante)
        divElement.style.display = 'none';
    } else if (divElement.style.display === 'none') {
        divElement.style.display = 'block';
    } else {
        divElement.style.display = 'none';
    }
}
function updateDivDisplay_2(modified_n_clicks_2) {
    var divElement = document.getElementById('X-heatmap-div');
    divElement.style.display = 'none'
}

// Enregistrez la fonction côté client pour être utilisée dans le callback
window.dash_clientside = {
    clientside: {
        updateDivDisplay: updateDivDisplay,
        updateDivDisplay_2: updateDivDisplay_2
    }
};

