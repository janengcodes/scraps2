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

    // State for when ingredient containers have been clicked
    const [activeContainers, setActiveContainers] = useState({})

    // State for ingredient data 
    const [ingredients, setIngredients] = useState([])

    // State for the filtered ingredients based on dropdown
    const [filteredIngredients, setFilteredIngredients] = useState([])

    // State for pantry ingredients
    const [pantryIngredients, setPantryIngredients] = useState([])

    // State for active ingredients
    const [activeIngredients, setActiveIngredients] = useState([])

    // State for the dropdown
    const [selectedFoodGroup, setSelectedFoodGroup] = useState("");

    // State for cuisine match
    const [cuisineMatch, setCuisineMatch] = useState([]);

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
        console.log("Drop down clicked", food_group);
        setSelectedFoodGroup(food_group)
        // Filter the ingredients based on the food group
        const filtered = ingredients.filter(
            (ingredient) => ingredient.food_group === food_group
        );
        setFilteredIngredients(filtered);
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
                const { pantry_ingredients } = response.data
                setPantryIngredients(pantry_ingredients || [])
                console.log("Pantry Ingredients:", pantryIngredients); // Log the state to check its value
                setCuisineMatch(response.data.recs || [])
            })
            .catch((error) => {
                console.error('Error fetching pantry data:', error);
            });
    }, [username]);

    const buttonActive2 = (ingredientID) => {
        setActiveContainers((prev) => ({
            ...prev,
            [ingredientID]: !prev[ingredientID], // Toggle active state by ID
        }));
      
        setActiveIngredients((prev) => {
          if (Array.isArray(prev)) {
            // Use the `prev` value of `setActiveContainers` to determine the toggle logic
            const isCurrentlyActive = prev.includes(ingredientID); // Check current ingredient state
            if (isCurrentlyActive) {
              return prev.filter((name) => name !== ingredientID); // Remove ingredient
            } else {
              return [...prev, ingredientID]; // Add ingredient
            }
          } else {
            return [ingredientID]; // Handle the case where it's not an array
          }
        });
      };
      
    
    const handleSubmit = () => {
        console.log("handleSubmit called");
    
        fetch(`/api/add-to-pantry/${username}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ ingredients: activeIngredients }),
        })
        .then((response) => {
            if (!response.ok) throw new Error("Failed to add ingredients");
            return response.json();
        })
        .then((data) => {
            console.log("Ingredients added successfully:", data);
    
            // Assuming the backend returns the updated pantry ingredients
            setPantryIngredients((prev) => [...prev, ...data.pantry_ingredients]);
            setCuisineMatch(data.recs || []);
            setActiveContainers({});
            setActiveIngredients([]);

        })
        .catch((error) => {
            console.error("Error:", error);
        });
    };
    


    return (

        <div className="main-container"> 
            <h2 className="ingredient-header">In Season Ingredients</h2>

            <div className="ingredient-header dropdown">
                <button className="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-expanded="false">
                    Select Ingredient Type
                </button>
                <ul className="dropdown-menu" aria-labelledby="dropdownMenuButton">
                    <li><a className="dropdown-item" href="#" onClick={() => dropDownClicked("veggies")}>Vegetables</a></li>
                    <li><a className="dropdown-item" href="#" onClick={() => dropDownClicked("fruit")}>Fruits</a></li>
                </ul>
            </div>

            <div className="in-season-box">
                {Array.isArray(filteredIngredients) &&
                filteredIngredients.map((ingredient, index) => (
                    <div
                    key={ingredient.ingredient_id}
                    className={`ingredient-container ${
                        activeContainers[ingredient.ingredient_id] ? "active" : ""
                    }`}
                    onClick={() => buttonActive2(ingredient.ingredient_id)}
                    >
                        <div>{ingredient.ingredient_name}</div>
                    </div>
                ))}
            </div>
        
            <button
                type="submit"
                className="submit"
                onClick={handleSubmit}
            >
                Add to My Pantry
            </button>



            <h2 className="ingredient-header">Ingredients</h2>
            <div className="outer-pantry">
                <div className="veggies-pantry">
                    <h2 className="ingredient-header">Veggies</h2>
                    <div className="pantry-ingredient-box">
                        {Array.isArray(pantryIngredients) && pantryIngredients
                            .filter((ingredient) => ingredient.food_group === "veggies") // Filter ingredients by food group
                            .map((ingredient, index) => (
                            <div className="pantry-ingredient">{ingredient.ingredient_name}</div>
                        ))}
                    </div>
                </div>
                <div className="fruits-pantry">
                    <h2 className="ingredient-header">Fruits</h2>
                    <div className="pantry-ingredient-box">
                        {Array.isArray(pantryIngredients) &&
                            pantryIngredients
                                .filter((ingredient) => ingredient.food_group === "fruit") // Filter ingredients by food group
                                .map((ingredient, index) => (
                                    <div key={index} className="pantry-ingredient">
                                        {ingredient.ingredient_name}
                                    </div>
                                ))}
                    </div>
                </div>
                <div className="protein-pantry">
                    <h2 className="ingredient-header">Proteins</h2>
                    <div className="pantry-ingredient-box">
                        {Array.isArray(pantryIngredients) && pantryIngredients
                            .filter((ingredient) => ingredient.food_group === "protein") // Filter ingredients by food group
                            .map((ingredient, index) => (
                            <div className="pantry-ingredient">{ingredient.ingredient_name}</div>
                        ))}
                    </div>
                </div>
                <div className="grains-pantry">
                    <h2 className="ingredient-header">Grains</h2>
                    <div className="pantry-ingredient-box">
                        {Array.isArray(pantryIngredients) && pantryIngredients
                            .filter((ingredient) => ingredient.food_group === "grains") // Filter ingredients by food group
                            .map((ingredient, index) => (
                            <div className="pantry-ingredient">{ingredient.ingredient_name}</div>
                        ))}
                    </div>
                </div>
            </div>

            <h2 className="ingredient-header">Cuisine Matches</h2>
            <div className="cuisine-match-box">
                {Array.isArray(cuisineMatch) &&
                cuisineMatch.map((match, index) => (
                    <div key={index} className="cuisine">
                        {match.cuisine} - {match.probability}%
                    </div>
                ))}
            </div>



                


        </div>

    );
}