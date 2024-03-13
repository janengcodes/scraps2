import React from "react";
import { createRoot } from "react-dom/client";
import Button from "react-bootstrap/Button"; // we can import elements like Button to the
//import LoggedInNavBar from "./NavBar";
import { StrictMode } from "react";
// import SavedRecipes from "./saved_recipes";
import LoggedInNavBar from "./NavBar";

// Create a root
const root = createRoot(document.getElementById("reactEntry"));

// This method is only called once
// Insert the post component into the DOM
root.render(
  <StrictMode>
    <LoggedInNavBar />
  </StrictMode>
);
