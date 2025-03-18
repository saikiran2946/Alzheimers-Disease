import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./Home";
import About from "./About";
import Contact from "./Contact";
import Auth from "./Auth"; // Importing Signup/Login page
import Prediction from "./Prediction";
import "./styles.css";

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/auth" element={<Auth />} />  {/* Sign Up/Login Page */}
        <Route path="/predict" element={<Prediction />} /> {/* Prediction Page */}
      </Routes>
    </Router>
  );
};

export default App;
