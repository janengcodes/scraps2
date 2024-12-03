import React, { useState, useEffect } from "react";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import { Button } from "react-bootstrap";
import '../static/css/pantry.css'
import '../static/css/globals.css'
import '../static/css/style.css'
import axios from 'axios';

export default function UserPantryIngredients() {
    console.log("Pantry Ingredients called")

    // Handle when buttons have been clicked
    const [activeContainers, setActiveContainers] = useState({})

    // Handle ingredient data 
    const [ingredients, setIngredients] = useState([])
    const username = localStorage.getItem("user");
    const inSeasonFoodGroup = "";
    // Active state for when a button is clicked on 
    const buttonActive = (index) => {
        console.log("buttonActive called")
        setActiveContainers((prevState) => ({
            ...prevState, 
            [index]: !prevState[index],
        }));
    };

    const dropDownClicked = (food_group) => {
        console.log("Drop down clicked");
        inSeasonFoodGroup = food_group;

    };

    // Fetch user's pantry data from the API 
    useEffect(() => {
        // Fetch the user's pantry data 
        // axiosHTTP requests to REST endpoints
        axios 
            .get(`/api/pantry/${username}`)
            .then((response) => {
                // Ingredients are the response data 
                const { ingredients } = response.data
                setIngredients(ingredients || [])
            })
            .catch((error) => {
                console.error('Error fetching pantry data:', error);
            });
    }, [username]);


    return (

        <div class="main-container"> 
            <h2 class="ingredient-header">In Season Ingredients for California, USA</h2>

            <div class="ingredient-header dropdown">
                <button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-expanded="false">
                    Select Ingredient Type
                </button>
                <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                    <li><a class="dropdown-item" href="#" onClick={() => dropDownClicked("Vegtables")}>Vegetables</a></li>
                    <li><a class="dropdown-item" href="#">Fruits</a></li>
                    <li><a class="dropdown-item" href="#">Protein</a></li>
                </ul>
            </div>

        
            <div className="in-season-box">
                {Array.isArray(ingredients) && ingredients.map((ingredient, index) => (
                    <div
                        key={index}
                        // Append the active class if the ingredient container is clicked
                        className={`ingredient-container ${activeContainers[index] ? 'active' : ''}`}
                        onClick={() => buttonActive(index)}
                    >
                        <p>{ingredient.ingredient_name}</p>
                    </div>
                ))}
            </div>

        
        <button type="submit" class="submit">Add to My Pantry</button>
        </div>

    );
}