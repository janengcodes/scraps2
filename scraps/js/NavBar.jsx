import React, { useState, useEffect } from "react";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import { Button } from "react-bootstrap";
import '../static/css/navbar.css'

export default function LoggedInNavBar() {
  console.log("nav bar called")
  const [user, setUser] = useState("");

  useEffect(() => {
    let ignoreStaleRequest = false;


  // Check if user info is already in local storage
  const storedUser = localStorage.getItem("user");
  if (storedUser) {
    setUser(storedUser);
    return;
  }

  // Fetch user info from API if not in local storage
  fetch("/api/check-auth", { credentials: "same-origin" })
    .then((response) => {
      if (!response.ok) throw new Error(response.statusText);
      return response.json();
    })
    .then((data) => {
      if (!ignoreStaleRequest && data.username) {
        setUser(data.username);
        localStorage.setItem("user", data.username); // Store user info in local storage
      }
    })
    .catch((error) => console.log("Error checking authentication:", error));

  return () => {
    ignoreStaleRequest = true;
  };
  }, []);

  const handleLogout = async () => {
    setUser(""); // Clear the user state
    localStorage.removeItem("user"); // Remove user info from local storage
    try {
      const response = await fetch('/accounts/logout/', {
        method: 'POST', // Use GET if the server expects it
        credentials: 'same-origin', // Include credentials if needed
      });
  
      if (response.ok) {
        console.log("Logged out successfully");
        window.location.href = '/'; // Redirect after logout
      } else {
        console.error("Logout failed");
      }
    } catch (error) {
      console.error("An error occurred during logout:", error);
    }
  };
  return (
    <Navbar collapseOnSelect expand="lg" className="bg-body-tertiary">
      <Container>
        <Navbar.Brand href="/">SCRAPS</Navbar.Brand>
        <Navbar.Toggle aria-controls="responsive-navbar-nav" />
        <Navbar.Collapse id="responsive-navbar-nav">
          <Nav className="ms-auto gap-3">
            {user ? (
              <>
                <Nav.Link eventKey={1} href="/select_ingredients">
                  Select Ingredients
                </Nav.Link>
                <Nav.Link eventKey={2} href={`/pantry/${user}`}>
                  Pantry
                </Nav.Link>
                <Nav.Link eventKey={3} href="/saved_recipes/">
                  Saved Recipes
                </Nav.Link>
                <Nav.Link eventKey={4} href={`/user/${user}`}>
                  My Profile
                </Nav.Link>
                <Button className="btn btn-light btn-logout" onClick={handleLogout} href="/accounts/logout/">
                  Log Out
                </Button>
              </>
            ) : (
              <>
                <Button variant="primary" href="/accounts/login/" className="me-2">
                  Log In
                </Button>
                <Button variant="outline-primary" href="/accounts/signup/">
                  Sign Up
                </Button>
              </>
            )}
          </Nav>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  );
}
