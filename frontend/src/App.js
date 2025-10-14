import { useState, useEffect } from "react";
import "@/App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import axios from "axios";
import HomePage from "@/pages/HomePage";
import Dashboard from "@/pages/Dashboard";
import AnalysisDetail from "@/pages/AnalysisDetail";
import { Toaster } from "@/components/ui/sonner";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
export const API = `${BACKEND_URL}/api`;

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/analysis/:id" element={<AnalysisDetail />} />
        </Routes>
      </BrowserRouter>
      <Toaster position="top-right" />
    </div>
  );
}

export default App;