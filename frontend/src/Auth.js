import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import "./Auth.css";

const Auth = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    confirmPassword: "",
    mobile: "",
  });

  const navigate = useNavigate();

  const toggleAuth = () => setIsLogin(!isLogin);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const validateEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  };

  const handleAuth = async () => {
    if (!validateEmail(formData.email)) {
      alert("Please enter a valid email address.");
      return;
    }

    if (!isLogin) {
      // Signup validations
      if (formData.password !== formData.confirmPassword) {
        alert("Passwords do not match!");
        return;
      }
      if (!/^\d{10}$/.test(formData.mobile)) {
        alert("Please enter a valid 10-digit mobile number.");
        return;
      }
    }

    const endpoint = isLogin ? "login" : "signup";
    try {
      const response = await axios.post(`http://127.0.0.1:5000/${endpoint}`, formData);
      alert(response.data.message);
      if (isLogin) navigate("/predict"); // Redirect to prediction page after login
    } catch (error) {
      alert(error.response?.data?.message || "Authentication failed");
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-box">
        <h2>{isLogin ? "Login" : "Sign Up"}</h2>
        
        {!isLogin && (
          <>
            <input type="text" name="name" placeholder="Full Name" value={formData.name} onChange={handleChange} required />
            <input type="tel" name="mobile" placeholder="Mobile Number" value={formData.mobile} onChange={handleChange} required />
          </>
        )}

        <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required />
        <input type="password" name="password" placeholder="Password" value={formData.password} onChange={handleChange} required />

        {!isLogin && (
          <input type="password" name="confirmPassword" placeholder="Confirm Password" value={formData.confirmPassword} onChange={handleChange} required />
        )}

        <button onClick={handleAuth}>{isLogin ? "Login" : "Sign Up"}</button>

        <p onClick={toggleAuth} className="toggle-text">
          {isLogin ? "Don't have an account? Sign Up" : "Already have an account? Login"}
        </p>
      </div>
    </div>
  );
};

export default Auth;
