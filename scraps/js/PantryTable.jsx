import React from "react";

import "../static/css/globals.css";
import "../static/css/style.css";
import "../static/css/pantry-table.css";
import axios from "axios";

export default function UserPantryTable() {
  console.log("Pantry table called");
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
              <li>Cabbage</li>
              <li>Romaine</li>

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
        </div>

        <div className="ingredient-section">
          <div className="ingredient-heading">
            <p className="space-mono-bold">Protein</p>
          </div>
        </div>

        <div className="ingredient-section">
          <div className="ingredient-heading">
            <p className="space-mono-bold">Grains</p>
          </div>
        </div>

        <div className="ingredient-section">
          <div className="ingredient-heading other-ingredients">
            <p className="space-mono-bold">Other</p>
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
