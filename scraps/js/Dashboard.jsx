import React from "react";
import { createRoot } from "react-dom/client";
import { StrictMode } from "react";
import MealCalendar from "./MealCalendar";

// Render the MealCalendar 
const elements = document.querySelectorAll(".reactEntryDashboard");
elements.forEach((element) => {
  const root = createRoot(element);
  root.render(
    <StrictMode>
      <MealCalendar />
    </StrictMode>
  );
});
