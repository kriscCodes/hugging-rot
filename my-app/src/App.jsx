import { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import './App.css';
import Home from './Home';
import EnterText from './EnterText';

function App() {
  return (
    <Router>
      <div className="navbar">
        <Link to="/">Home</Link>
        <Link to="/enter-text">Enter Your Text</Link>
      </div>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/enter-text" element={<EnterText />} />
      </Routes>
    </Router>
  );
}

export default App;
