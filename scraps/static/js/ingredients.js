function printMessage(message) {
  console.log(message);
}

printMessage("This is a message printed to the console.");

// get all the buttons

// var elements = new Map();
// elements.set("produceButton", ["produce", "produceHeading"]);
// elements.set("proteinButton", ["protein", "proteinHeading"]);
// elements.set("dairyButton", ["dairy", "dairyHeading"]);
// elements.set("grainsButton", ["grains", "grainsHeading"]);

function deleteGrids(clickedButton) {
  var elements = new Map();
  elements.set("produceButton", ["produce", "produceHeading"]);
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
      ingredient.style.display = "none";
      heading.style.display = "none";
    }
  }
}
