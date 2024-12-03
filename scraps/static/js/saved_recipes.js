function printMessage(message) {
    console.log(message);
}
  
printMessage("This is a message printed to the console.");


function checkCardClick() {
    console.log("Recipe card was clicked");
}

// If a recipe box is clicked, then maximize it 
function maximizeRecipe(clickedRecipe) {
    console.log("Maximizing Recipe")
    clickedRecipe.classList.add('recipe-clicked');
}

function minimizeRecipe(clickedRecipe) {
    console.log("Mini Recipe")
    clickedRecipe.classList.add('recipe-clicked');
}