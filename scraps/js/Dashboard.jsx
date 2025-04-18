// Dashboard.jsx
import React, { useState, useEffect } from "react";
import MealCalendar from "./MealCalendar";
import ShoppingList from "./ShoppingList";

export default function Dashboard() {
  const [meals, setMeals] = useState([]);
  const [ingredients, setIngredients] = useState([]);

  return (
    <>
      <MealCalendar meals={meals} setMeals={setMeals} />
      <ShoppingList ingredients={ingredients} setIngredients={setIngredients} meals={meals} />
    </>
  );
}
