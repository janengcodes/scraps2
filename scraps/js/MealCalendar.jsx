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
  const [formValues, setFormValues] = useState({ mealType: "", mealName: "" });

  const handleDayClick = (day) => {
    setSelectedDay(day === selectedDay ? null : day); // Toggle form
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
  const renderForm = () => (
    <form onSubmit={handleSubmit} className="meal-form mt-2">
      <div className="form-group mb-2">
        <label>Meal Type</label>
        <input
          type="text"
          name="mealType"
          className="form-control"
          value={formValues.mealType}
          onChange={handleChange}
          placeholder="e.g. Breakfast"
        />
      </div>
      <div className="form-group mb-2">
        <label>Meal Name</label>
        <input
          type="text"
          name="mealName"
          className="form-control"
          value={formValues.mealName}
          onChange={handleChange}
          placeholder="e.g. Blueberry Pancakes"
        />
      </div>
      <button type="submit" className="btn btn-primary">Save Meal</button>
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
                <div className="center day" 
                      key={day}
                      onClick={() => handleDayClick(day)}>
                  <th>{day}</th>
                  {selectedDay === day && renderForm()}
                </div>
              )
            )}
          </div>
        </div>
      </div>

     
        <div className="selected-day-details mt-4">
          <h2 className="h2-be-vietnam-pro">{selectedDay}'s Details</h2>
          <p className="space-mono-regular">You clicked on <strong>{selectedDay}</strong>. Here you can show more meal info.</p>
        </div>
      

      <h2 className="h2-be-vietnam-pro shopping-list-header">Shopping List</h2>
    </div>
  );
}
