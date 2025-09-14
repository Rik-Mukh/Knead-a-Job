import React, { useState, useEffect } from 'react';
import gmailService from '../services/gmailService';

const GmailMessages = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchMessages = async () => {
        try {
            setLoading(true);
            setError(null);
            const result = await gmailService.fetchMessages();
            setMessages(result.messages || []);
        } catch (error) {
            console.error('Error fetching Gmail messages:', error);
            
            // Better error handling
            if (error.response) {
            // Server responded with an error status
            if (error.response.status === 401) {
                setError('Please log in to access your Gmail messages.');
            } else if (error.response.status === 400 && error.response.data.error) {
                setError(`Gmail error: ${error.response.data.error}`);
            } else {
                setError(`Error: ${error.response.status} ${error.response.statusText}`);
            }
            } else if (error.request) {
            // Request made but no response
            setError('Server not responding. Please try again later.');
            } else {
            // Something else went wrong
            setError('Failed to load Gmail messages. Please try again later.');
            }
        } finally {
            setLoading(false);
        }
    };

  useEffect(() => {
    fetchMessages();
  }, []);

  if (loading) {
    return (
      <div style={{ padding: '36px', maxWidth: '800px', margin: '0 auto' }}>
        <h1 style={{ marginBottom: '20px', font: "normal 500 2.5rem helvetica-neue-lt-pro" }}>Gmail Messages</h1>
        <p>Loading messages...</p>
      </div>
    );
  }

  return (
    <div style={{ padding: '36px', maxWidth: '800px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1 style={{ margin: 0, font: "normal 500 2.5rem helvetica-neue-lt-pro" }}>Gmail Messages</h1>
        <button
          className="btn btn-primary"
          onClick={fetchMessages}
          disabled={loading}
        >
          {loading ? 'Loading...' : 'Refresh'}
        </button>
      </div>
      
      {error ? (
        <div style={{ 
          padding: '16px', 
          backgroundColor: '#f8d7da', 
          color: '#721c24', 
          border: '1px solid #f5c6cb', 
          borderRadius: '4px',
          marginBottom: '16px'
        }}>
          {error}
        </div>
      ) : null}
      
      {messages.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <p>No Gmail messages found</p>
        </div>
      ) : (
        <div>
          <p style={{ marginBottom: '16px', color: '#666' }}>
            Showing {messages.length} message{messages.length !== 1 ? 's' : ''}
          </p>
          {messages.map(message => (
            <div 
              key={message.id} 
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "flex-start",
                backgroundColor: '#f5f5f5',
                padding: '12px 24px',
                marginBottom: '8px',
                borderRadius: '12px',
                boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
              }}
            >
              <h4 style={{ margin: '0 0 4px 0', font: "normal 500 1.5rem helvetica-neue-lt-pro" }}>{message.subject}</h4>
              <div style={{ margin: '4px 0', fontSize: '14px' }}>
                <strong>From:</strong> {message.sender}
              </div>
              <p style={{ margin: '0 0 4px 0', fontSize: '14px', color: '#555' }}>{message.snippet}</p>
              <span style={{ marginTop: '16px', fontSize: '12px', color: '#888' }}>
                {new Date(message.date).toLocaleString()}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default GmailMessages;