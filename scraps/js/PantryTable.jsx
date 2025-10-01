import React, { useState, useEffect } from "react";

import "../static/css/globals.css";
import "../static/css/style.css";
import "../static/css/pantry-table.css";
import axios from "axios";

export default function UserPantryTable() {
// Ingredient data
const [ingredients, setIngredients] = useState([]);
// Pantry ingredients 
const [pantryIngredients, setPantryIngredients] = useState([]); 
// Username 
const username = localStorage.getItem("user");

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

          })
          .catch((error) => {
              console.error('Error fetching pantry data:', error);
          });
  }, [username]);

  // Values check, keep separate so that we don't see old pantry ingredients 
  useEffect(() => {
    console.log("Pantry Ingredients updated:", pantryIngredients);
  }, [pantryIngredients]);

  return (
    <>
    <div className="pantry-layout">
      <div className="ingredients-cell">
        <div className="main-ingredient-form">
          <form action="" className="my-form">
            <label
              htmlFor="ingredient"
              className="be-vietnam-pro-smaller label-main"
            >
              Add a new ingredient
            </label>
            <br />
            <div className="form-input-fields">
              <input
                type="text"
                id="fingredientmain"
                className="be-vietnam-pro-smaller"
                name="fingredientmain"
              />
              <input type="submit" className="submit-main" value="Add" />
            </div>
          </form>
        </div>

        <div className="ingredient-section">
          <div className="ingredient-heading">
            <p className="space-mono-bold">Veggies</p>
          </div>
          <div className="ingredient-list">
            <ul className="a be-vietnam-pro-smaller">
                {Array.isArray(pantryIngredients) && pantryIngredients
                    .filter((ingredient) => ingredient.food_group === "veggies") // Filter ingredients by food group
                    .map((ingredient, index) => (
                    <div className="pantry-ingredient">{ingredient.ingredient_name}</div>
                ))}
              <li>
                <form
                  action=""
                  className="ingredient-form fade-in my-form"
                >
                  {/* <label htmlFor="ingredient">Ingredient:</label> */}
                  <div className="ingredient-form-block">
                    <ul className="a">
                      <li>
                        <input
                          type="text"
                          id="fingredient"
                          className="be-vietnam-pro-smaller"
                          name="fingredient"
                        />
                        <br />
                        <br />
                      </li>
                    </ul>
                    <input
                      type="submit"
                      value="Add"
                      className="submit-not-main"
                    />
                  </div>
                </form>
              </li>
            </ul>
          </div>
        </div>

        <div className="ingredient-section">
          <div className="ingredient-heading">
            <p className="space-mono-bold">Fruits</p>
          </div>
          <div className="ingredient-list">
            <ul className="a be-vietnam-pro-smaller">
                {Array.isArray(pantryIngredients) && pantryIngredients
                    .filter((ingredient) => ingredient.food_group === "fruit") // Filter ingredients by food group
                    .map((ingredient, index) => (
                    <div className="pantry-ingredient">{ingredient.ingredient_name}</div>
                ))}
              <li>
                <form
                  action=""
                  className="ingredient-form fade-in my-form"
                >
                  {/* <label htmlFor="ingredient">Ingredient:</label> */}
                  <div className="ingredient-form-block">
                    <ul className="a">
                      <li>
                        <input
                          type="text"
                          id="fingredient"
                          className="be-vietnam-pro-smaller"
                          name="fingredient"
                        />
                        <br />
                        <br />
                      </li>
                    </ul>
                    <input
                      type="submit"
                      value="Add"
                      className="submit-not-main"
                    />
                  </div>
                </form>
              </li>
            </ul>
          </div>
        </div>

  

        <div className="ingredient-section">
          <div className="ingredient-heading">
            <p className="space-mono-bold">Protein</p>
          </div>
           <div className="ingredient-list">
            <ul className="a be-vietnam-pro-smaller">
                {Array.isArray(pantryIngredients) && pantryIngredients
                    .filter((ingredient) => ingredient.food_group === "protein") // Filter ingredients by food group
                    .map((ingredient, index) => (
                    <div className="pantry-ingredient">{ingredient.ingredient_name}</div>
                ))}
              <li>
                <form
                  action=""
                  className="ingredient-form fade-in my-form"
                >
                  {/* <label htmlFor="ingredient">Ingredient:</label> */}
                  <div className="ingredient-form-block">
                    <ul className="a">
                      <li>
                        <input
                          type="text"
                          id="fingredient"
                          className="be-vietnam-pro-smaller"
                          name="fingredient"
                        />
                        <br />
                        <br />
                      </li>
                    </ul>
                    <input
                      type="submit"
                      value="Add"
                      className="submit-not-main"
                    />
                  </div>
                </form>
              </li>
            </ul>
          </div>


        </div>

        <div className="ingredient-section">
          <div className="ingredient-heading">
            <p className="space-mono-bold">Grains</p>
          </div>
           <div className="ingredient-list">
            <ul className="a be-vietnam-pro-smaller">
                {Array.isArray(pantryIngredients) && pantryIngredients
                    .filter((ingredient) => ingredient.food_group === "grains") // Filter ingredients by food group
                    .map((ingredient, index) => (
                    <div className="pantry-ingredient">{ingredient.ingredient_name}</div>
                ))}
              <li>
                <form
                  action=""
                  className="ingredient-form fade-in my-form"
                >
                  {/* <label htmlFor="ingredient">Ingredient:</label> */}
                  <div className="ingredient-form-block">
                    <ul className="a">
                      <li>
                        <input
                          type="text"
                          id="fingredient"
                          className="be-vietnam-pro-smaller"
                          name="fingredient"
                        />
                        <br />
                        <br />
                      </li>
                    </ul>
                    <input
                      type="submit"
                      value="Add"
                      className="submit-not-main"
                    />
                  </div>
                </form>
              </li>
            </ul>
          </div>
        </div>

        <div className="ingredient-section">
          <div className="ingredient-heading other-ingredients">
            <p className="space-mono-bold">Other</p>
          </div>

           <div className="ingredient-list">
            <ul className="a be-vietnam-pro-smaller">
                {Array.isArray(pantryIngredients) && pantryIngredients
                    .filter((ingredient) => ingredient.food_group !== "fruit" && ingredient.food_group !== "protein" && ingredient.food_group !== "grains" && ingredient.food_group !== "veggies" ) // Filter ingredients by food group
                    .map((ingredient, index) => (
                    <div className="pantry-ingredient">{ingredient.ingredient_name}</div>
                ))}
              <li>
                <form
                  action=""
                  className="ingredient-form fade-in my-form"
                >
                  {/* <label htmlFor="ingredient">Ingredient:</label> */}
                  <div className="ingredient-form-block">
                    <ul className="a">
                      <li>
                        <input
                          type="text"
                          id="fingredient"
                          className="be-vietnam-pro-smaller"
                          name="fingredient"
                        />
                        <br />
                        <br />
                      </li>
                    </ul>
                    <input
                      type="submit"
                      value="Add"
                      className="submit-not-main"
                    />
                  </div>
                </form>
              </li>
            </ul>
          </div>

        </div>
      </div>

      <div className="pantry-info-cell">
        <div className="pie-chart">
          <div className="pie-chart-heading">
            <p className="space-mono-bold">Stats</p>
          </div>
        </div>
        <div className="cuisine-matches">
          <div className="cuisine-matches-heading">
            <p className="space-mono-bold">Looking for a new cuisine?</p>
          </div>
        </div>
      </div>

      <div className="in-season-ingredients-cell">
        <div className="isi-heading">
          <p className="space-mono-bold">
            In Season Ingredients for Denver, Colorado
          </p>
        </div>
      </div>
    </div>
    </>
  );
}
