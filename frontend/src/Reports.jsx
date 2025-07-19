import React, { useState, useEffect } from 'react';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function Reports() {
  const [dailyReports, setDailyReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchReports();
  }, []);

  const fetchReports = async () => {
    try {
      const response = await fetch(`${API_URL}/reports/daily`);
      const data = await response.json();
      setDailyReports(data.daily_reports);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching reports:', error);
      setMessage('Error loading reports');
      setLoading(false);
    }
  };

  const updateAttendance = async (enrollmentId, status) => {
    try {
      const response = await fetch(`${API_URL}/attendance/${enrollmentId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ enrollment_id: enrollmentId, attendance_status: status })
      });
      
      if (response.ok) {
        setMessage(`Attendance updated successfully`);
        // Refresh reports to show updated data
        fetchReports();
      } else {
        setMessage('Error updating attendance');
      }
    } catch (error) {
      console.error('Error updating attendance:', error);
      setMessage('Error updating attendance');
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'present': return '#4caf50';
      case 'absent': return '#f44336';
      case 'not_set': return '#ff9800';
      default: return '#666';
    }
  };

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  if (loading) return <div>Loading reports...</div>;

  return (
    <div className="reports-container">
      <h2>Daily Enrollment Reports</h2>
      
      {message && <div className="message info">{message}</div>}
      
      {dailyReports.length === 0 ? (
        <p>No enrollment data available.</p>
      ) : (
        dailyReports.map((dayReport) => (
          <div key={dayReport.date} className="day-report">
            <div className="day-header">
              <h3>{formatDate(dayReport.date)}</h3>
              <div className="day-stats">
                <span className="stat-item">
                  <strong>Total Enrollments:</strong> {dayReport.total_enrollments}
                </span>
                <span className="stat-item present">
                  <strong>Present:</strong> {dayReport.present}
                </span>
                <span className="stat-item absent">
                  <strong>Absent:</strong> {dayReport.absent}
                </span>
                <span className="stat-item not-set">
                  <strong>Not Set:</strong> {dayReport.not_set}
                </span>
              </div>
            </div>
            
            <div className="enrollments-list">
              {dayReport.enrollments.map((enrollment) => (
                <div key={enrollment.id} className="enrollment-item">
                  <div className="enrollment-info">
                    <span className="email">{enrollment.email}</span>
                    <span className="activity">{enrollment.activity}</span>
                  </div>
                  <div className="attendance-controls">
                    <span 
                      className="status-badge"
                      style={{ backgroundColor: getStatusColor(enrollment.attendance_status) }}
                    >
                      {enrollment.attendance_status.replace('_', ' ')}
                    </span>
                    <div className="attendance-buttons">
                      <button 
                        className="attendance-btn present-btn"
                        onClick={() => updateAttendance(enrollment.id, 'present')}
                        disabled={enrollment.attendance_status === 'present'}
                      >
                        Mark Present
                      </button>
                      <button 
                        className="attendance-btn absent-btn"
                        onClick={() => updateAttendance(enrollment.id, 'absent')}
                        disabled={enrollment.attendance_status === 'absent'}
                      >
                        Mark Absent
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))
      )}
    </div>
  );
}

export default Reports;