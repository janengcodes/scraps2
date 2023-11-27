import React, { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import MyComponent from "./saved_recipes";
import 'bootstrap/dist/css/bootstrap.css';


// Create a root
const root = createRoot(document.getElementById("saved_recipe"));

// This method is only called once
// Insert the post component into the DOM
root.render(
  <StrictMode>
    <MyComponent/>
  </StrictMode>,
);
