function deleteGrids(clickedButton) {
  var elements = new Map();
  elements.set("fruitButton", ["fruit", "fruitHeading"]);
  elements.set("veggiesButton", ["veggies", "veggiesHeading"]);
  elements.set("proteinButton", ["protein", "proteinHeading"]);
  elements.set("dairyButton", ["dairy", "dairyHeading"]);
  elements.set("grainsButton", ["grains", "grainsHeading"]);

  for (var [key, value] of elements) {

    var buttons = document.querySelectorAll('.button-2');
    buttons.forEach(function(btn) {
      btn.classList.remove('button-clicked');
    });
    buttons.forEach(function(btn) {
      btn.classList.remove('produce-init');
    });
    clickedButton.classList.add('button-clicked');


    var ingredient = document.getElementById(value[0]);
    var heading = document.getElementById(value[1]);
    if (key === clickedButton.id) {
      ingredient.style.display = "grid";
      heading.style.display = "block";
    } else {
      console.log("Hiding ingredient:", value[0]);
      ingredient.style.display = "none";
      heading.style.display = "none";
    }
  }
}
