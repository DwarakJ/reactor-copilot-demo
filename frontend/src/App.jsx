
import React, { useState, useEffect } from 'react';
import './index.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [activities, setActivities] = useState([]);
  const [featured, setFeatured] = useState([]);
  const [selectedActivity, setSelectedActivity] = useState('');
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetch(`${API_URL}/activities`)
      .then(res => res.json())
      .then(data => {
        setActivities(data.activities);
        setFeatured(data.featured);
      });
  }, []);

  const filteredActivities = activities;

  const handleSubmit = async e => {
    e.preventDefault();
    if (!email || !selectedActivity) {
      setMessage('Please enter your email and select an activity.');
      return;
    }
    const res = await fetch(`${API_URL}/enroll`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, team: selectedActivity })
    });
    const data = await res.json();
    setMessage(data.message);
    setEmail('');
    setSelectedActivity('');
  };

  return (
    <>
      <header>
        <h1>ABC Sports Centre</h1>
        <h2>Public Activity Enrollment</h2>
      </header>
      <div className="main-layout">
        <div className="main-content">
        <section id="highlighted-activities">
          <h4>Featured Activities</h4>
          <ul id="featured-list">
            {featured.map(activity => (
              <li key={activity}>{activity}</li>
            ))}
          </ul>
        </section>

        <section id="activities-container">
          <h3>Available Activities</h3>
          <div id="activities-list">
            {filteredActivities.length === 0 ? (
              <p>No activities found.</p>
            ) : (
              filteredActivities.map(activity => (
                <div className="activity-card" key={activity}>
                  <h4>{activity}</h4>
                  <p>Schedule: See centre for details</p>
                  <button onClick={() => setSelectedActivity(activity)}>
                    Select
                  </button>
                </div>
              ))
            )}
          </div>
        </section>
      </div>

      <aside id="signup-container">
        <h3>Enroll in an Activity</h3>
        <form id="signup-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Your Email:</label>
            <input
              type="email"
              id="email"
              required
              placeholder="your-email@example.com"
              value={email}
              onChange={e => setEmail(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label htmlFor="activity">Select Activity:</label>
            <select
              id="activity"
              required
              value={selectedActivity}
              onChange={e => setSelectedActivity(e.target.value)}
            >
              <option value="">-- Select an activity --</option>
              {filteredActivities.map(activity => (
                <option key={activity} value={activity}>{activity}</option>
              ))}
            </select>
          </div>
          <button type="submit">Enroll</button>
        </form>
        {message && <div id="message" className="message info">{message}</div>}
      </aside>
    </div>
  </>
  );
}

export default App;
