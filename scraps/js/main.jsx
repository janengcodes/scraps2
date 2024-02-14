import React from "react";
import { createRoot } from "react-dom/client";
import Button from "react-bootstrap/Button"; // we can import elements like Button to the 
//import LoggedInNavBar from "./NavBar";
import React, { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import SavedRecipes from "./saved_recipes";


// Create a root
const root = createRoot(document.getElementById("reactEntry"));

// This method is only called once
// Insert the post component into the DOM
root.render(

  <StrictMode>
    {/* <Post url="/api/v1/posts/"/> */}
    <SavedRecipes url="/api/v1/saved_recipes/" />
  </StrictMode>,
);

