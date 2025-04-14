import React, { useState, useEffect } from "react";
import Container from "react-bootstrap/Container";
import Nav from "react-bootstrap/Nav";
import Navbar from "react-bootstrap/Navbar";
import { Button } from "react-bootstrap";
import '../static/css/globals.css'
import '../static/css/style.css'
import '../static/css/dashboard.css'
import axios from 'axios';

export default function MealCalendar() {
  const [selectedDay, setSelectedDay] = useState(null);
  const [formValues, setFormValues] = useState({ mealType: "", mealName: "", selectedRecipe: ""});
  const [recipes, setRecipes] = useState([]);


  useEffect(() => {
    axios.get('/api/saved_recipes/')
      .then((res) => {
        setRecipes(res.data); // assuming Flask returns a list (not an object with a key)
      })
      .catch((err) => {
        console.error("Error fetching recipes:", err);
      });
  }, []);

  const handleDayClick = (day) => {
    setSelectedDay(
      day = day
    ); 
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormValues(prev => ({ ...prev, [name]: value }));
  };

  

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(`Submitted for ${selectedDay}:`, formValues);
    // Optionally reset or close form
    setSelectedDay(null);
    setFormValues({ mealType: "", mealName: "" });
  };

  const renderNewMeal = () => (
    console.log("Saving new meal...")
    // {/* <div className="center day">
    //   <p className="center">Sunday</p>
    //   <div className="meal">
    //     <h4 className="meal-type">Breakfast</h4>
    //     <p className="meal-name">Blueberry Pancakes</p>
    //     <div className="recipe-link-container">
    //       <p className="recipe-link">View Recipe</p>
    //     </div>
    //   </div>
    // </div> */}
  );

  const renderForm = () => (
    <form onSubmit={handleSubmit} className="meal-form">
      
      {/* Meal Type */}
      <div className="">
        <input
          type="text"
          name="mealType"
          className="form-control meal-form-input"
          value={formValues.mealType}
          onChange={handleChange}
          placeholder="Meal Type"
        />
      </div>

      {/* Meal Name */}
      <div className="">
        <input
          type="text"
          name="mealName"
          className="form-control meal-form-input"
          value={formValues.mealName}
          onChange={handleChange}
          placeholder="Recipe Name"
        />
      </div>

      {/* Dropdown */}
      <select
        name="selectedRecipe"
        className="meal-form-input meal-form-dropdown"
        onChange={handleChange}
      >
        <option value="">Select Recipe</option>
        {recipes && recipes.map((recipe) => (
          <option key={recipe.recipe_id} value={recipe.name}>
            {recipe.name}
          </option>
        ))}

      </select>

      <button 
        type="submit" 
        className="submit-meal-form"
        onClick={() => renderNewMeal()}
      >Save</button>
    </form>

  );

  return (
    <div className="container-fluid p-4">
      <h1 className="h1-be-vietnam-pro text-center dashboard-heading">Dashboard</h1>

      <div className="meal-calendar">
        <div className="meal-calendar-header">
          <div className="meal-calendar-text">
            <h2 className="h2-be-vietnam-pro">Meal Calendar</h2>
            <h3 className="space-mono-bold meal-calendar-dates">April 1 - April 8</h3>
          </div>
        </div>

        <div className="meal-calendar-body">
          <div className="table">
            {/* <div className="center day">
              <p className="center">Sunday</p>
              <div className="meal">
                <h4 className="meal-type">Breakfast</h4>
                <p className="meal-name">Blueberry Pancakes</p>
                <div className="recipe-link-container">
                  <p className="recipe-link">View Recipe</p>
                </div>
              </div>
            </div> */}

            {["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"].map(
              (day) => (
                <div className="center day" 
                      key={day}
                      onClick={() => handleDayClick(day)}>
                  <p className="center">{day}</p>
                  {selectedDay === day && renderForm()}
                </div>
              )
            )}
          </div>
        </div>
      </div>
      

      <h2 className="h2-be-vietnam-pro shopping-list-header">Shopping List</h2>
    </div>
  );
}
