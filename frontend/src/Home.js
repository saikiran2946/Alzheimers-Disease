import React from "react";
import { useNavigate } from "react-router-dom";
import "./Home.css";

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      {/* Navigation Bar */}
      <div className="navbar">
        <button onClick={() => navigate("/about")}>About</button>
        <button onClick={() => navigate("/contact")}>Contact</button>
        <button onClick={() => navigate("/auth")}>Predict</button>
      </div>

      {/* Main Content */}
      <div className="content">
        <h1>Alzheimer’s Disease Prediction</h1>
        <p>Early Detection Can Save Lives. Get a quick and reliable detection.</p>
        <button className="predict-button" onClick={() => navigate("/auth")}>
          Get Started
        </button>
      </div>
    </div>
  );
};

export default Home;
