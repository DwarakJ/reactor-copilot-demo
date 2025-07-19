
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import Enrollment from './Enrollment';
import Reports from './Reports';
import './index.css';

function Navigation() {
  const location = useLocation();
  
  return (
    <nav className="navigation">
      <Link 
        to="/" 
        className={location.pathname === '/' ? 'nav-link active' : 'nav-link'}
      >
        Activity Enrollment
      </Link>
      <Link 
        to="/reports" 
        className={location.pathname === '/reports' ? 'nav-link active' : 'nav-link'}
      >
        Reports & Attendance
      </Link>
    </nav>
  );
}

function App() {
  return (
    <Router>
      <>
        <header>
          <h1>ABC Sports Centre</h1>
          <h2>Public Activity Enrollment & Management</h2>
          <Navigation />
        </header>
        
        <main>
          <Routes>
            <Route path="/" element={<Enrollment />} />
            <Route path="/reports" element={<Reports />} />
          </Routes>
        </main>
      </>
    </Router>
  );
}

export default App;
