import React from "react";
import "./About.css";

const About = () => {
  return (
    <div className="about-container">
      <h1 className="about-heading">Understanding Alzheimer's Disease</h1>
      
      <div className="about-content">
        <p>
          Alzheimer's disease is a **progressive neurological disorder** that affects millions worldwide. 
          It gradually impairs memory, cognitive functions, and the ability to perform daily tasks. 
          Early detection can play a crucial role in slowing down the progression and managing symptoms effectively.
        </p>
      </div>

      <div className="about-section">
        <h2>What is Alzheimer's Disease?</h2>
        <p>
          Alzheimer's is a form of **dementia** that leads to a decline in memory and reasoning abilities. 
          It is caused by abnormal protein build-up in the brain, leading to **neuronal damage and loss of connections** 
          between brain cells.
        </p>
      </div>

      <div className="about-section">
        <h2>Effects of Alzheimer's</h2>
        <p>
          This disease significantly impacts both the patient and their caregivers. 
          Some common effects include:
        </p>
        <ul>
          <li>Gradual **memory loss** and confusion</li>
          <li>Difficulty in problem-solving and decision-making</li>
          <li>Changes in mood, behavior, and personality</li>
          <li>Loss of ability to perform daily activities</li>
        </ul>
      </div>

      <div className="about-section">
        <h2>Why Early Detection Matters?</h2>
        <p>
          Identifying Alzheimer's at an early stage allows for **better treatment options, 
          improved quality of life, and effective long-term planning**. 
          Our AI-based system helps in detecting Alzheimer's through advanced **machine learning models**.
        </p>
      </div>

      <div className="about-section">
        <h2>Common Risk Factors</h2>
        <ul>
          <li>Age: The biggest risk factor, usually affecting people over 65</li>
          <li>Genetics: Family history increases susceptibility</li>
          <li>Lifestyle Factors: Poor diet, lack of exercise, and smoking</li>
          <li>Medical Conditions: High cholesterol, diabetes, and hypertension</li>
        </ul>
      </div>

      <div className="about-section">
        <h2>How Can We Help?</h2>
        <p>
          Our **Alzheimer's Disease Detection System** uses AI-driven predictions to assess cognitive 
          patterns and provide insights into **potential risks**. By leveraging machine learning, we 
          offer an efficient way to **identify early symptoms**, aiding in early diagnosis.
        </p>
      </div>
    </div>
  );
};

export default About;
