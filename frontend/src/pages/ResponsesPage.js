import React, { useEffect, useState } from 'react';
import { applicationService } from '../services/applicationService';

const ResponsesPage = () => {
  const [responses, setResponses] = useState([]);

  useEffect(() => {
    applicationService.getAll().then(data => {
      const filtered = data.filter(app => app.meeting_minutes);
      setResponses(filtered);
    });
  }, []);

  return (
    <div>
      <h1>Responses / Meeting Minutes</h1>
      {responses.map((app) => (
        <div key={app.id} style={{ marginBottom: '1rem', borderBottom: '1px solid #ccc' }}>
          <h3>{app.position} at {app.company_name}</h3>
          <p><strong>Meeting Minutes:</strong></p>
          <p>{app.meeting_minutes}</p>
        </div>
      ))}
    </div>
  );
};

export default ResponsesPage;
