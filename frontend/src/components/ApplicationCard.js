import React from 'react';

const ApplicationCard = ({ application, onEdit, onDelete, onTrack, onAddMeetingMinutes }) => {
  const getStatusColor = (status) => {
    switch (status) {
      case 'applied': return '#EFEFEF';
      case 'interview': return '#C8F1FF';
      case 'rejected': return '#FFCDCD';
      case 'accepted': return '#E1FFCD';
      case 'withdrawn': return '#6c757d';
      default: return '#6c757d';
    }
  };

  const showOpts = (e) => {
    const card = e.target.closest(".application-card");
    const wrapper = card.querySelector(".app-button-wrapper")
    wrapper.style.visibility="visible";
    wrapper.style.height="48px"
  }

  const hideOpts = (e) => {
    const card = e.target.closest(".application-card");
    const wrapper = card.querySelector(".app-button-wrapper")
    wrapper.style.visibility="hidden";
    wrapper.style.height="0px"
  }

  const onMouseOverBtn = (e) => {
    e.target.style.backgroundColor ="#333"
    e.target.style.color = "white"
  }

  const onMouseOutBtn = (e) => {
    e.target.style.backgroundColor =""
    e.target.style.color = ""
  }

  const onMouseOverBtn2 = (e) => {
    e.target.style.backgroundColor ="#ff4c4c"
  }

  const onMouseOutBtn2 = (e) => {
    e.target.style.backgroundColor ="#ff8b8b"
  }

  const dateOptions = {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', dateOptions);
  };

  const handleCardClick = () => {
    if (application.job_url) {
      window.open(application.job_url, '_blank');
    }
  };

  return (
    <div 
    className="application-card" 
    onClick={handleCardClick}
    onMouseOver={showOpts}
    onMouseOut={hideOpts}>
      <div className="app-info-wrapper">
        <div className="app-info">
          <div className="app-text">
            Applied on {formatDate(application.applied_date)}
          </div>
          <div className="app-text" style={{
            color: "black",
            fontSize: "20px",
          }}>
            {application.position} @ <span style={{
              fontWeight: 700,
              color: "#03a5fc"
            }}>
              {application.company_name}
              </span>
          </div>
          <div className="app-text">
            {application.location}
          </div>
          <div className="app-text" style={{
            fontWeight: "500",
          }}>
            {application.salary_range}
          </div>
        </div>
        <div className="app-info" style={{
          alignItems: "flex-end",
          width: "fit-content",
        }}>
          <div className="app-status app-text" style={{
            backgroundColor: getStatusColor(application.status),
            color: "black",
            borderRadius: "8px"
          }}>
            {(application.status).charAt(0).toUpperCase() + (application.status).slice(1)}
          </div>
        </div>
      </div>
      <div className="notes wrapper" style={{
        display: "flex",
        flexDirection: "column",
        gap: "4px",
        width: "100%"
      }}>
        <div className = "app-notes app-text" style={{
          color: "black",
          padding: "0px 16px 0px 16px",
          fontSize: "14px",
        }}>{application.notes}</div>
        <div 
          className="app-button-wrapper"
          style={{
            visibility: "hidden",
            height: 0
          }}>
          <button 
          className="application-btn"
          onClick={(e) => { e.stopPropagation(); onTrack(application); }}
          onMouseOver={onMouseOverBtn}
          onMouseOut={onMouseOutBtn}>
            Track Responses
          </button>
          <button 
          className="application-btn"
          onClick={(e) => { e.stopPropagation(); onAddMeetingMinutes(application); }}
          onMouseOver={onMouseOverBtn}
          onMouseOut={onMouseOutBtn}>
            Add Minutes
          </button>
          <button 
          className="application-btn" 
          onClick={(e) => { e.stopPropagation(); onEdit(application); }}
          onMouseOver={onMouseOverBtn}
          onMouseOut={onMouseOutBtn}>
            Edit
          </button>
          <button 
          className="application-btn" 
          style={{
            backgroundColor: "#ff8b8b"
          }}
          onClick={(e) => { e.stopPropagation(); onDelete(application); }}
          onMouseOver={onMouseOverBtn2}
          onMouseOut={onMouseOutBtn2}>
            Delete
          </button>
        </div>
      </div>

    </div>
  )
};

export default ApplicationCard;
