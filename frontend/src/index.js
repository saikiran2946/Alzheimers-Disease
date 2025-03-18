import React from "react";
import App from "./App";
import "./styles.css";


import { createRoot } from "react-dom/client";
const root = createRoot(document.getElementById("root"));
root.render(<App />);
import { BrowserRouter } from "react-router-dom";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

const router = createBrowserRouter([
  { path: "/", element: <Home /> },
  { path: "/login", element: <Login /> },
  { path: "/signup", element: <Signup /> },
  { path: "/predict", element: <Prediction /> },
]);

<RouterProvider router={router} future={{ v7_startTransition: true, v7_relativeSplatPath: true }} />;
