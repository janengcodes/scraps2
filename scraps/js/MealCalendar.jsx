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
  const [meals, setMeals] = useState([]); 
  const username = localStorage.getItem("user");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedDay) return;
  
    const newMeal = {
      day: selectedDay,
      mealType: formValues.mealType,
      mealName: formValues.mealName,
      selectedRecipe: formValues.selectedRecipe
    };
  
    try {
      const response = await axios.post(`/api/add-to-meal-cal/${username}`, newMeal);
      console.log('Meal saved to database:', response.data);
  
      setMeals((prevMeals) => [...prevMeals, newMeal]);
  
      setFormValues({
        mealType: '',
        mealName: '',
        selectedRecipe: ''
      });
    } catch (error) {
      console.error('Error saving meal:', error);
    }
  };
  

  useEffect(() => {
    axios.get('/api/saved_recipes/')
      .then((res) => {
        setRecipes(res.data); // assuming Flask returns a list (not an object with a key)
      })
      .catch((err) => {
        console.error("Error fetching recipes:", err);
      });
  }, []);

  useEffect(() => {
    const fetchMeals = async () => {
      try {
        const res = await axios.get(`/api/add-to-meal-cal/${username}`);
        setMeals(res.data);
      } catch (err) {
        console.error("Error fetching meals:", err);
      }
    };

    fetchMeals();
  }, [username]);

  const handleDayClick = (day) => {
    setSelectedDay(
      day = day
    ); 
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormValues(prev => ({ ...prev, [name]: value }));
  };

  


  

  const renderNewMeal = (day) => {
    // filter out the meals
    const mealsForDay = meals.filter(meal => meal.day === day)

    return (
      <div className="meal-list">
        {mealsForDay.map((meal, index) => (
          <div key={index} className="meal">
            <h4 className="meal-type">{meal.mealType}</h4>
            <p className="meal-name">{meal.mealName}</p>

            <div className="recipe-link-container">
              <p className="recipe-link">{meal.selectedRecipe}</p>
              
            </div>
          </div>
        ))}
      </div>
    );
  };

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

  const getCurrentWeek = () => {
    const today = new Date();
    const dayOfWeek = today.getDay(); // 0 (Sunday) to 6 (Saturday)
  
    const start = new Date(today);
    start.setDate(today.getDate() - dayOfWeek); // Set to Sunday
  
    const end = new Date(today);
    end.setDate(today.getDate() + (6 - dayOfWeek)); // Set to Saturday
  
    const options = { month: 'long', day: 'numeric' };
  
    const startStr = start.toLocaleDateString('en-US', options);
    const endStr = end.toLocaleDateString('en-US', options);
  
    return `${startStr} - ${endStr}`;
  } 

  // const renderMealsForDay = (day) => {
  //   return meals
  //     .filter(meal => meal.meal_day === day)
  //   // // filter out the meals
  //   // const mealsForDay = meals.filter(meal => meal.day === day)

  //   // return (
  //   //   <div className="meal-list">
  //   //     {mealsForDay.map((meal, index) => (
  //   //       <div key={index} className="meal">
  //   //         <h4 className="meal-type">{meal.mealType}</h4>
  //   //         <p className="meal-name">{meal.mealName}</p>

  //   //         <div className="recipe-link-container">
  //   //           <p className="recipe-link">{meal.selectedRecipe}</p>
              
  //   //         </div>
  //   //       </div>
  //   //     ))}
  //   //   </div>
  //   // );
  //     .map((meal, index) => (
  //         <div key={index} className="meal">
  //           <h4 className="meal-type ">{meal.mealType}</h4>
  //           <p className="meal-name meal-name-db">{meal.mealName}</p>
  //           <div className="recipe-link-container recipe-link-container-db">
  //             <p className="recipe-link">{meal.selectedRecipe}</p>
  //           </div>
  //       </div>
  //     ));
  // };

  const renderMealsForDay = (day) => {
    const mealsForDay = meals.filter(meal => meal.meal_day === day);
    return (
      <div className="meal-list">
        {mealsForDay.map((meal, index) => (
          <div key={index} className="meal">
            <h4 className="meal-type ">{meal.mealType}</h4>
            <p className="meal-name">{meal.mealName}</p>
            <div className="recipe-link-container">
              <p className="recipe-link">{meal.selectedRecipe}</p>
            </div>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="container-fluid p-4">
      <h1 className="h1-be-vietnam-pro text-center dashboard-heading">Dashboard</h1>

      <div className="meal-calendar">
        <div className="meal-calendar-header">
          <div className="meal-calendar-text">
            <h2 className="h2-be-vietnam-pro">Meal Calendar</h2>
            <h3 className="space-mono-bold meal-calendar-dates">{getCurrentWeek()}</h3>
          </div>
        </div>

        <div className="meal-calendar-body">
          <div className="table">
          {["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"].map(
          (day) => (
            <div className="center day" key={day} onClick={() => handleDayClick(day)}>
              <p className="center">{day}</p>

              {/* Display existing meals from DB */}
              {renderMealsForDay(day)}

              {/* New meal preview or form */}
              {renderNewMeal(day)}
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
