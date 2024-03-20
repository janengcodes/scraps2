import React from "react";
import { createRoot } from "react-dom/client";
import Button from "react-bootstrap/Button";
import { StrictMode } from "react";
import LoggedInNavBar from "./NavBar";

// Render the component in the first container
const root = createRoot(document.getElementById("reactEntry"));
root.render(
  <StrictMode>
    <LoggedInNavBar />
  </StrictMode>
);

// Render the component in the second container
const rootHomePage = createRoot(document.getElementById("reactEntryHome"));
rootHomePage.render(
  <StrictMode>
    <LoggedInNavBar />
  </StrictMode>
);
