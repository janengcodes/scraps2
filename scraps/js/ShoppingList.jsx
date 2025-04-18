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


export default function ShoppingList({ ingredients, setIngredients, meals }) {
    // const [ingredients, setIngredients] = useState([])
    const [shoppingListIngredients, setShoppingListIngredients] = useState([])
    const username = localStorage.getItem("user");
    // fetch the user's pantry data
    useEffect(() => {
        // Fetch the user's pantry data 
        // axiosHTTP requests to REST endpoints
        axios 
            .get(`/api/currentPantry/${username}`)
            .then((response) => {
                const { ingredient_names } = response.data;
                const formatted = ingredient_names.map((name) => ({ ingredient_name: name }));
                setIngredients(formatted || []);
                setShoppingListIngredients(formatted || []);
                console.log('Fetched ingredient names:', formatted);
            })
            .catch((error) => {
                console.error('Error fetching pantry data:', error);
            });
    }, [username]);

    const daysOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

    return (
        <div className="container-fluid p-4">
            <div className="shopping-list-grid">
                <div className="shopping-list-header">
                    <div className="shopping-list-text">
                        <h2 className="h2-be-vietnam-pro shopping-list-heading-text">🛒 Shopping List</h2>
                    </div>
                </div>
                {/* all of the days in the week stored into day-column to hold the ingredients
                (currently on every day) */}
                <div className="grid-system">
                    <div className="day-column">
                        <h3 className="space-mono-bold weekly-shopping-list">Weekly Shopping List</h3>
                        {shoppingListIngredients.length === 0 ? (
                                <p>You're all set! ✅</p>
                            ) : (
                                <ul className="shopping-list-items">
                                    {shoppingListIngredients.map((item, i) => (
                                        <li key={i} className="shopping-list-item">
                                            <label>
                                                <input type="checkbox" />
                                                <span>{item.ingredient_name}</span>
                                            </label>
                                        </li>
                                    ))}
                                </ul>
                        )}
                    </div>
                    {daysOfWeek.map((day, index) => (
                        <div key={index} className="day-column">
                            <div className="day-cell">{day}</div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
}