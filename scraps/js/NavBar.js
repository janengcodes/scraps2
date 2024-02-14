import React from "react";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
// import "/static/css/style.css";
// import NavDropdown from "react-bootstrap/NavDropdown";



function LoggedInNavBar() {
  return (
    <Navbar collapseOnSelect expand="lg" className="bg-body-tertiary">
      <Container>
        <Navbar.Brand href="/index2">
          Scraps <img src="/static/images/carrot.png" className="carrot" style={{ width: "50px", height: "50px" }}/>{" "}
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
        <Nav className="me-auto"></Nav>
          <Nav>
            <Nav.Link href="/recipes">Recipes</Nav.Link>
            <Nav.Link eventKey={2} href="/saved_recipes">
              Saved Recipes
            </Nav.Link>
            <Nav.Link eventKey={3} href="/user">
              My Profile
            </Nav.Link>
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}

export default LoggedInNavBar;

{
  /* <Nav className="me-auto">
  <Nav.Link href="#features">Features</Nav.Link>
  <Nav.Link href="#pricing">Pricing</Nav.Link>
  <NavDropdown title="Dropdown" id="collapsible-nav-dropdown">
    <NavDropdown.Item href="#action/3.1">Action</NavDropdown.Item>
    <NavDropdown.Item href="#action/3.2">
      Another action
    </NavDropdown.Item>
    <NavDropdown.Item href="#action/3.3">Something</NavDropdown.Item>
    <NavDropdown.Divider />
    <NavDropdown.Item href="#action/3.4">
      Separated link
    </NavDropdown.Item>
  </NavDropdown>
</Nav> */
}