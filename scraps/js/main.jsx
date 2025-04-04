import React from "react";
import { createRoot } from "react-dom/client";
import Button from "react-bootstrap/Button";
import { StrictMode } from "react";
import LoggedInNavBar from "./NavBar";
import UserPantryIngredients from "./PantryIngredients";

// Render the LoggedInNavBar 
const elements = document.querySelectorAll(".reactEntry");
elements.forEach((element) => {
  const root = createRoot(element);
  root.render(
    <StrictMode>
      <LoggedInNavBar />
    </StrictMode>
  );
});


// Render the LoggedInNavBar 
const pantry_elements = document.querySelectorAll(".pantryReactEntry");
pantry_elements.forEach((element) => {
  const root = createRoot(element);
  root.render(
    <StrictMode>
      <LoggedInNavBar />
      <UserPantryIngredients />
    </StrictMode>
  );
});
