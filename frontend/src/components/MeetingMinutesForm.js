import React, { useState, useEffect } from 'react';
import { meetingNotesService } from '../services/meetingNotesService';

const MeetingMinutesForm = ({ application, onClose, onSuccess }) => {
  const [meetingMinutes, setMeetingMinutes] = useState('');
  const [loading, setLoading] = useState(false);
  const [existingNotes, setExistingNotes] = useState([]);

  useEffect(() => {
    // Load existing meeting notes for this application
    const loadExistingNotes = async () => {
      try {
        const notes = await meetingNotesService.getByApplication(application.id);
        setExistingNotes(notes);
        // If there are existing notes, show the most recent one
        if (notes.length > 0) {
          setMeetingMinutes(notes[0].content);
        }
      } catch (error) {
        console.error('Error loading existing notes:', error);
      }
    };
    loadExistingNotes();
  }, [application.id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!meetingMinutes.trim()) return;

    setLoading(true);
    try {
      await meetingNotesService.create(application.id, {
        content: meetingMinutes
      });
      onSuccess && onSuccess();
      onClose();
    } catch (error) {
      console.error('Error saving meeting minutes:', error);
      alert('Error saving meeting minutes. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0,0,0,0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000
    }}>
      <div className="modal-content" style={{
        backgroundColor: 'white',
        padding: '20px',
        borderRadius: '8px',
        maxWidth: '600px',
        width: '90%',
        maxHeight: '80vh',
        overflow: 'auto'
      }}>
        <h3>Add Meeting Minutes - {application.position} at {application.company_name}</h3>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group" style={{ marginBottom: '20px' }}>
            <label htmlFor="meetingMinutes" className="form-label">
              Meeting Minutes / Notes:
            </label>
            <textarea
              id="meetingMinutes"
              value={meetingMinutes}
              onChange={(e) => setMeetingMinutes(e.target.value)}
              className="form-control"
              rows="8"
              placeholder="Enter meeting notes, interview feedback, or any other relevant information..."
              style={{ width: '100%', resize: 'vertical' }}
            />
          </div>
          
          <div style={{ display: 'flex', gap: '10px', justifyContent: 'flex-end' }}>
            <button
              type="button"
              onClick={onClose}
              className="btn btn-secondary"
              disabled={loading}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading || !meetingMinutes.trim()}
            >
              {loading ? 'Saving...' : 'Save Meeting Minutes'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default MeetingMinutesForm;
