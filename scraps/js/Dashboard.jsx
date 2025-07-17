// Dashboard.jsx
import React, { useState, useEffect } from "react";
import MealCalendar from "./MealCalendar";
import ShoppingList from "./ShoppingList";

export default function Dashboard() {
  const [meals, setMeals] = useState([]);
  const [ingredients, setIngredients] = useState([]);
  // watch for changes to meals and then update ingredients accordingly
  // useEffect that updates ingredients based on meals 

  return (
    <>
      <MealCalendar meals={meals} setMeals={setMeals} />
      <ShoppingList ingredients={ingredients} setIngredients={setIngredients} meals={meals} />
    </>
  );
}
