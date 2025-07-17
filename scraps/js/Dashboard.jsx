// Dashboard.jsx
import React, { useState, useEffect } from "react";
import MealCalendar from "./MealCalendar";
import ShoppingList from "./ShoppingList";

export default function Dashboard() {
  const [meals, setMeals] = useState([]);
  const [ingredients, setIngredients] = useState([]);
  const [refreshTrigger, setRefreshTrigger] = useState(false);
  // watch for changes to meals and then update ingredients accordingly
  // useEffect that updates ingredients based on meals 
  const triggerRefresh = () => setRefreshTrigger(prev => !prev);

  return (
    <>
      <MealCalendar 
        meals={meals} 
        setMeals={setMeals} 
        refreshTrigger={refreshTrigger}   
        triggerRefresh={triggerRefresh} 
      />
      <ShoppingList 
        ingredients={ingredients} 
        setIngredients={setIngredients} 
        meals={meals} 
        refreshTrigger={refreshTrigger}
      />
    </>
  );
}
