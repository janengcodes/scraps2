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
            <div className="center day">
              <th>Sunday</th>
              <div className="meal">
                <h4 className="meal-type">Breakfast</h4>
                <p className="meal-name">Blueberry Pancakes</p>
                <div className="recipe-link-container">
                  <p className="recipe-link">View Recipe</p>
                </div>
              </div>
            </div>

            {["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"].map(
              (day) => (
                <div className="center day" key={day}>
                  <th>{day}</th>
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
