import React from "react";
import { createRoot } from "react-dom/client";
import Button from "react-bootstrap/Button"; // we can import elements like Button to the 
// import { CollapsibleExample } from "./NavBar";
import LoggedInNavBar from "./NavBar";
// import "bootstrap/dist/css/bootstrap.min.css";

const root = createRoot(document.getElementById("reactEntry")); // Use createRoot directly
const SimpleComponent = () => {
  return (
    <div>
      <div><LoggedInNavBar /> </div>
      <div>Hello, I'm a simple component!</div>
      <div>
        <Button>Test</Button>
      </div>
    </div>
  );
};

root.render(<SimpleComponent />);
