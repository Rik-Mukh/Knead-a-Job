import React, { useEffect, useState } from 'react';
import { applicationService } from '../services/applicationService';
import { meetingNotesService } from '../services/meetingNotesService';

const ResponsesPage = () => {
  const [responses, setResponses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchResponses();
  }, []);

  const fetchResponses = async () => {
    try {
      setLoading(true);
      // Get all meeting notes
      const meetingNotesResponse = await meetingNotesService.getAll();
       // Normalize response: use results if present, otherwise assume it's already an array
      const meetingNotes = meetingNotesResponse.results || meetingNotesResponse || [];
      
      // Get all applications to match with meeting notes
      const applications = await applicationService.getAll();
      
      // Create a map of application ID to application data
      const appMap = {};
      applications.forEach(app => {
        appMap[app.id] = app;
      });
      
      // Combine meeting notes with application data
      const responsesWithApps = meetingNotes.map(note => ({
        ...note,
        application: appMap[note.job_application]
      })).filter(item => item.application); // Only include notes with valid applications
      
      setResponses(responsesWithApps);
    } catch (error) {
      console.error('Error fetching responses:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: "numeric",
      month: "long",
      day: "numeric"
    });
  };

  if (loading) {
    return (
      <div className="text-center">
        <h1 style={{font: "normal 500 2.5rem helvetica-neue-lt-pro"}}>Responses / Meeting Minutes</h1>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div style={{padding: "20px"}}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px',}}>
        <h1 style={{font: "normal 500 2.5rem helvetica-neue-lt-pro"}}>Meeting Minutes</h1>
        <button 
          onClick={fetchResponses}
          className="btn btn-primary"
        >
          Refresh
        </button>
      </div>

      {responses.length > 0 ? (
        <div className="grid grid-1" >
          {responses.map((note) => (
            <div key={note.id} className="card" style={{ marginBottom: '20px', border: 'none',boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '15px', }}>
                <div>
                  <h3 style={{ 
                    margin: '0 0 8px 0', 
                    fontWeight: "500",
                    fontSize: "1.5rem",
                    color: "black",}}
                      className="app-text">
                    {note.application.position} @  
                    <span style={{fontWeight: "700", color: '#03a5fc'}}> {note.application.company_name}</span>
                    </h3>
                  <p style={{ margin: '0', color: '#666' }}>
                    Applied on {formatDate(note.application.applied_date)}
                  </p>
                </div>
                <span
                  style={{
                    backgroundColor: note.application.status === 'interview' ? '#C8F1FF' : 
                                   note.application.status === 'accepted' ? '#E1FFCD' : 
                                   note.application.status === 'rejected' ? 'FFCDCD' : '#17a2b8',
                    color: 'black',
                    padding: '4px 8px',
                    borderRadius: '12px',
                    fontSize: '12px',
                    textTransform: 'capitalize'
                  }}
                >
                  {note.application.status}
                </span>
              </div>
              
              <div style={{ 
                backgroundColor: '#f8f9fa', 
                padding: '15px', 
                borderRadius: '8px',
                border: '1px solid #e9ecef',
                boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
                
              }}>
                <h5 style={{ margin: '0 0 10px 0', color: '#495057' }}>Meeting Minutes:</h5>
                <p style={{ margin: '0', whiteSpace: 'pre-wrap', lineHeight: '1.5' }}>
                  {note.content}
                </p>
              </div>

              <p style={{ width: "100%", alignContent: 'flex-end', margin: '0', color: '#666', fontSize: '16px' }}>
                    {formatDate(note.created_at)}
              </p>

            </div>
          ))}
        </div>
      ) : (
        <div className="card text-center">
          <h3>No Meeting Minutes Found</h3>
          <p style={{ color: '#666' }}>
            You haven't added any meeting minutes yet. Go to the Applications page and click "Add Meeting Minutes" on any job application to get started!
          </p>
        </div>
      )}
    </div>
  );
};

export default ResponsesPage;
