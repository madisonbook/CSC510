//import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import './App.css'
import LandingPage from './components/LandingPage';
import Dashboard from './components/Dashboard';
import { Button } from "./components/ui/button"
import EmailVerification from './components/EmailVerification';

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/verify" element={<EmailVerification />} />
      </Routes>
    </Router>
  );
}

export default App
