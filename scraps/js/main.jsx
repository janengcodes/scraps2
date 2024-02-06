import React from "react";
import { createRoot } from "react-dom/client";
import Button from "react-bootstrap/Button"; // we can import elements like Button to the 
import "bootstrap/dist/css/bootstrap.min.css";

const root = createRoot(document.getElementById("reactEntry")); // Use createRoot directly
const SimpleComponent = () => {
  return <div>Hello, I'm a simple component!</div>;
};

root.render(<SimpleComponent />);
