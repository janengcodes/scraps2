import React, { useState, useEffect } from "react";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import { Button } from "react-bootstrap";
import '../static/css/pantry.css'
import '../static/css/globals.css'
import '../static/css/style.css'

export default function UserPantryIngredients() {
    console.log("Pantry Ingredients called")
    return (

        <div class="main-container"> 
            <h2 class="ingredient-header">In Season Ingredients for California, USA</h2>

            <div class="ingredient-header dropdown">
                <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-expanded="false">
                    Select Ingredient Type
                </button>
                <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                    <li><a class="dropdown-item" href="#">Vegetables</a></li>
                    <li><a class="dropdown-item" href="#">Fruits</a></li>
                    <li><a class="dropdown-item" href="#">Meat</a></li>
                </ul>
            </div>

        
            <div class="in-season-box">
                <div class="ingredient-container"></div>
                <div class="ingredient-container"></div>
                <div class="ingredient-container"></div>
                <div class="ingredient-container"></div>
                <div class="ingredient-container"></div>
            </div>
        
        <button type="submit" class="submit">Add to My Pantry</button>
        </div>

    );
}