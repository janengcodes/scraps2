import React, { useState, useEffect } from "react";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import { Button } from "react-bootstrap";
import '../static/css/globals.css'
import '../static/css/style.css'
import '../static/css/shopping-list.css'
import axios from 'axios';
// Get the ingredients that the user still needs from the recipe


export default function ShoppingList() {
    const [ingredients, setIngredients] = useState([])
    const [pantryIngredients, setPantryIngredients] = useState([])
    const [shoppingListIngredients, setShoppingListIngredients] = useState([])
    const username = localStorage.getItem("user");
    // fetch the user's pantry data
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

                // ✅ Get list of pantry ingredient IDs
                const pantryIds = pantry_ingredients.map(i => i.ingredient_id);
                // ✅ Filter ingredients to find what's still needed
                const needed = ingredients.filter(item => !pantryIds.includes(item.ingredient_id));
                // ✅ Update shopping list state
                setShoppingListIngredients(needed);
            })
            .catch((error) => {
                console.error('Error fetching pantry data:', error);
            });
    }, [username]);


    return (
    <div className="container-fluid p-4">
        <div className="shopping-list-grid">
            <div className="shopping-list-header">
                <div className="shopping-list-text">
                    <h2 className="h2-be-vietnam-pro shopping-list-heading-text">Shopping List</h2>
                </div>
                
            </div>
            <div>
                {shoppingListIngredients.length === 0 ? (
                    <p>You're all set! ✅</p>
                ) : (
                    <ul className="shopping-list-items">
                    
                    {shoppingListIngredients.map((item, index) => (
                        <li key={index} className="shopping-list-item">
                        <label>
                            <input type="checkbox" />
                            <span>{item.ingredient_name}</span>
                        </label>
                        </li>
                    ))}
                    </ul>
                )}
            </div>

        </div>
    </div>

   

        

    );
}
    