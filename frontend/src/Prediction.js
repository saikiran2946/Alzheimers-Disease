import React, { useState } from "react";
import axios from "axios";
import "./Prediction.css";

const Prediction = () => {
  const [features, setFeatures] = useState({
    Age: "",
    BMI: "",
    DietQuality: "",
    SleepQuality: "",
    CholesterolTotal: "",
    CholesterolHDL: "",
    CholesterolTriglycerides: "",
    MMSE: "",
    FunctionalAssessment: "",
    MemoryComplaints: "",
    ADL: "",
    BehavioralProblems: "",
  });

  const [prediction, setPrediction] = useState(null);

  const handleChange = (e) => {
    setFeatures({ 
      ...features, 
      [e.target.name]: e.target.value === "" ? "" : Number(e.target.value) 
    });
  };

  const handlePrediction = async () => {
    try {
      const featureValues = Object.values(features).map(value => Number(value));

      console.log("📨 Sending features:", featureValues);  // Debugging log

      const response = await axios.post("http://localhost:5000/predict", { features: featureValues });

      console.log("📩 Received response:", response.data);  // Debugging log
      setPrediction(response.data.prediction);

    } catch (error) {
      console.error("❌ Error in Prediction:", error);
      alert("Prediction failed. Check the inputs and try again.");
    }
  };

  return (
    <div className="prediction-container">
      <h2 className="prediction-title">Alzheimer’s Disease Prediction</h2>
      <div className="input-form">
        {Object.keys(features).map((key, index) => (
          <div key={index} className="input-group">
            <label htmlFor={key}>{key}:</label>
            <input 
              id={key} 
              type="number" 
              name={key} 
              placeholder={`Enter ${key}`} 
              value={features[key]} 
              onChange={handleChange} 
            />
          </div>
        ))}
      </div>
      <button className="predict-btn" onClick={handlePrediction}>Predict</button>
      {prediction && <div className="result-box">Result: {prediction}</div>}
    </div>
  );
};

export default Prediction;
