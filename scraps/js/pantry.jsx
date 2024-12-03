import React from "react";
import { createRoot } from "react-dom/client";
import Button from "react-bootstrap/Button";
import { StrictMode } from "react";
import UserPantryIngredients from "./PantryIngredients";

// Render the LoggedInNavBar 
const elements = document.querySelectorAll(".pantryReactEntry");
elements.forEach((element) => {
  const root = createRoot(element);
  root.render(
    <StrictMode>
      <UserPantryIngredients />
    </StrictMode>
  );
});
