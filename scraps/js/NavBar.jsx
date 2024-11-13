import React from "react";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import { useState, useEffect } from "react";
import { Button } from "react-bootstrap";

export default function LoggedInNavBar({}) {
  const [user, setUser] = useState("");

  useEffect(() => {
    let ignoreStaleRequest = false;

    fetch("/api/check-auth", { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        if (!ignoreStaleRequest) {
          setUser(data.fullname); // Assuming 'data.fullname' contains user's name
        }
      })
      .catch((error) => console.log(error));

    return () => {
      ignoreStaleRequest = true;
    };
  }, []);

  return (
    <Navbar collapseOnSelect expand="lg" className="bg-body-tertiary">
      <Container>
        <Navbar.Brand href="/">
          Scraps{" "}
          {/* <img
            src="/static/images/carrot.png"
            className="carrot"
            style={{ width: "50px", height: "50px" }}
            alt="carrot icon"
          /> */}
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="me-auto"></Nav>
          <Nav>
            <Nav.Link href="/select_ingredients">Select Ingredients</Nav.Link>
            <Nav.Link eventKey={2} href="/select_ingredients">
            </Nav.Link>
            
            <Nav.Link href="/pantry">Pantry</Nav.Link>

            <Nav.Link eventKey={2} href="/saved_recipes">
              Saved Recipes
            </Nav.Link>
            {user ? (
              <Nav.Link eventKey={3} href={`/user/${user}`}>
                Welcome, {user}
              </Nav.Link>
            ) : (
              <Button variant="primary" href="/accounts/login/">
                Log In
              </Button>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}
