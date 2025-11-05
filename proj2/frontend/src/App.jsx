//import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import './App.css'
import LandingPage from './components/LandingPage';
import Dashboard from './components/Dashboard';
import { Button } from "./components/ui/button"

import './styles/globalstyles.css';

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}

export default App
