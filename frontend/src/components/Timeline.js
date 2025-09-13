import React from "react";
import "./Timeline.css";

const Timeline = ({ isOpen, onClose, application }) => {
  if (!isOpen || !application) return null;

  const events = [
    { key: "applied_date", label: "Application Date" },
    { key: "interview_one", label: "Interview One" },
    { key: "interview_two", label: "Interview Two" },
    { key: "offer_date", label: "Offer" },
  ];

  const visibleEvents = events.filter((e) => application[e.key]);

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        className="modal-card"
        onClick={(e) => e.stopPropagation()} 
      >
        <div className="modal-header">
          <h3>{application.company_name} Timeline</h3>
          <button className="close-btn" onClick={onClose}>
            ✕
          </button>
        </div>

        <div className="timeline-container">
          <div className="timeline-line" />
          {visibleEvents.length === 0 && (
            <p style={{ textAlign: "center", color: "#666" }}>
              No timeline data available.
            </p>
          )}
          {visibleEvents.map((e) => (
            <div key={e.key} className="timeline-item">
              <div className="timeline-dot" />
              <div className="timeline-content">
                <strong>{e.label}:</strong>
                <div>
                  {new Date(application[e.key]).toLocaleDateString(undefined, {
                    year: "numeric",
                    month: "short",
                    day: "numeric", 
                  })}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Timeline;
