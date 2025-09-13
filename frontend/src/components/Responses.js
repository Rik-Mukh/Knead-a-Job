import React, { useEffect, useState } from 'react';
import { applicationService } from '../services/applicationService';

const Responses = () => {
  const [applications, setApplications] = useState([]);

  useEffect(() => {
    const fetchApps = async () => {
      const data = await applicationService.getAllDetailed(); // This should return meeting_minutes
      setApplications(data);
    };
    fetchApps();
  }, []);

  const handleSave = async (id, newMinutes) => {
    await applicationService.update(id, { meeting_minutes: newMinutes });
    setApplications(prev =>
      prev.map(app =>
        app.id === id ? { ...app, meeting_minutes: newMinutes } : app
      )
    );
  };

  return (
    <div className="responses-page">
      <h2>Responses & Meeting Minutes</h2>
      {applications.map((app) => (
        <div key={app.id} className="card mb-3" >
          <h4>{app.company_name} - {app.position}</h4>
          <textarea
            rows="5"
            value={app.meeting_minutes || ''}
            onChange={(e) =>
              setApplications(prev =>
                prev.map(a =>
                  a.id === app.id
                    ? { ...a, meeting_minutes: e.target.value }
                    : a
                )
              )
            }
            style={{ width: '100%', padding: '10px', }}
          />
          <button
            onClick={() => handleSave(app.id, app.meeting_minutes)}
            className="btn btn-primary mt-2"
          >
            Save Notes
          </button>
        </div>
      ))}
    </div>
  );
};

export default Responses;
