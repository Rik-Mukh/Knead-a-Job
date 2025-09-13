import React, { useState, useEffect } from "react";
import Timeline from "../components/Timeline"; 
import { applicationService } from "../services/applicationService";
import { resumeService } from "../services/resumeService";
import Confetti from 'react-confetti';

import "./Dashboard.css";

// Status mapping with colors
const STATUS_MAP = {
  offer: { label: "Offer", color: "#E1FFCD" },
  accepted: { label: "Accepted", color: "#E1FFCD" },
  applied: { label: "Applied", color: "#EFEFEF" },
  interview: { label: "Interview", color: "#C8F1FF" },
  rejected: { label: "Rejected", color: "#FFCDCD" },
  withdrawn: { label: "Withdrawn", color: "#6c757d" },
};

// Statistic cards mapping
const STATCARD_MAP = {
  applied: { label: "Job", color: "#EFEFEF" },
  interview: { label: "Interview", color: "#C8F1FF" },
  rejected: { label: "Rejection", color: "#FFCDCD" },
  offer: { label: "Offer", color: "#E1FFCD" },
  accepted: { label: "Accepted", color: "#E1FFCD" },
};

// Status badge component
const StatusBadge = ({ status }) => {
  if (!status) return null;
  const key = status.toLowerCase();
  const s = STATUS_MAP[key] || { label: status, color: "#6c757d" };
  return (
    <span 
      className="status-badge" 
      style={{ 
        backgroundColor: s.color, 
        padding: "4px 8px",
        borderRadius: "12px",
        textTransform: "capitalize",
        fontSize: "12px"
      }}
    >
      {s.label}
    </span>
  );
};

// Statistic card component
const StatisticCard = ({ type, count }) => {
  const stat = count !== 1 ? `${STATCARD_MAP[type].label}s` : STATCARD_MAP[type].label;
  return (
    <div
      className="statCard"
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "flex-end",
        justifyContent: "space-between",
        backgroundColor: STATCARD_MAP[type].color,
        color: "black",
        width: "100%",
        height: "100%",
        padding: "24px",
        boxSizing: "border-box",
        borderRadius: "24px"
      }}
    >
      <div style={{ font: "normal 400 6.25rem helvetica-neue-lt-pro" }}>{count}</div>
      <div style={{ font: "normal 300 2rem helvetica-neue-lt-pro" }}>{stat}</div>
    </div>
  );
};

// Format date helper
const formatDate = (dateString) => {
  if (!dateString) return "";
  const dt = new Date(dateString);
  return dt.toLocaleDateString(undefined, {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

const Dashboard = () => {
  const [recentApplications, setRecentApplications] = useState([]);
  const [defaultResume, setDefaultResume] = useState(null);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({ applied: 0, interviews: 0, rejected: 0, offers: 0 });
  const [selectedApp, setSelectedApp] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const applications = await applicationService.getAll();
        setRecentApplications(applications);

        const resume = await resumeService.getDefault();
        setDefaultResume(resume);

        // Update stats
        setStats({
          applied: applications.length,
          interviews: applications.filter(app => app.status.toLowerCase() === "interview").length,
          rejected: applications.filter(app => app.status.toLowerCase() === "rejected").length,
          offers: applications.filter(app => ["offer", "accepted"].includes(app.status.toLowerCase())).length,
        });
      } catch (err) {
        console.error("Failed to fetch dashboard data", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  // Confetti if any "Offer" or "Accepted"
  const hasOffer = recentApplications.some(app => ["offer", "accepted"].includes(app.status.toLowerCase()));
  const width = window.innerWidth;
  const height = window.innerHeight;

  if (loading) {
    return (
      <div className="dashboard-wrap">
        <h2>Dashboard</h2>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div className="dashboard-wrap" style={{ position: "relative" }}>
      {hasOffer && <Confetti width={width} height={height} numberOfPieces={200} recycle={false} />}

      {/* Hero */}
      <div className="dashboard-hero">
        <div className="hero-date">{formatDate(new Date())}</div>
        <h1 className="hero-title">So far, you’ve applied to...</h1>
      </div>

      {/* Statistics */}
      <section
        className="stat-wrapper"
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          width: "100%",
          height: "16.75rem",
          padding: "10px",
          gap: "16px"
        }}
      >
        <StatisticCard type="applied" count={stats.applied} />
        <StatisticCard type="interview" count={stats.interviews} />
        <StatisticCard type="rejected" count={stats.rejected} />
        <StatisticCard type="offer" count={stats.offers} />
      </section>

      {/* Applications Table */}
      <div className="table-card" style={{ marginTop: "24px" }}>
        <table className="app-table" aria-label="Recent applications">
          <thead>
            <tr>
              <th>Company Name</th>
              <th>Position</th>
              <th>Date Applied</th>
              <th>Status</th>
              <th>Resume</th>
            </tr>
          </thead>
          <tbody>
            {recentApplications.length === 0 && (
              <tr>
                <td colSpan="5" style={{ textAlign: "center", padding: "24px", color: "#777" }}>
                  No applications yet.
                </td>
              </tr>
            )}
            {recentApplications.map(app => (
              <tr key={app.id || app.company_name + app.applied_date}>
                <td>{app.company_name}</td>
                <td>{app.position}</td>
                {/* Date Applied opens timeline, no URL style */}
                <td 
                  style={{ cursor: "default", color: "#000" }}
                  onClick={() => setSelectedApp(app)}
                >
                  {formatDate(app.applied_date)}
                </td>
                <td><StatusBadge status={app.status} /></td>
                <td>
                  <a href={app.resume_url || "#"} target="_blank" rel="noopener noreferrer" onClick={e => e.stopPropagation()}>
                    {app.resume_file || "Resume.pdf"}
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Default Resume Card */}
      {defaultResume && (
        <div style={{ marginTop: "24px" }}>
          <div className="table-card">
            <h4>{defaultResume.title}</h4>
            <p style={{ color: "#666", fontSize: "14px" }}>
              Uploaded: {formatDate(defaultResume.created_at)}
            </p>
            <button className="btn btn-primary" onClick={() => window.open(defaultResume.file_url, "_blank")}>
              Download Resume
            </button>
          </div>
        </div>
      )}

      {/* Timeline Modal */}
      <Timeline isOpen={!!selectedApp} onClose={() => setSelectedApp(null)} application={selectedApp} />
    </div>
  );
};

export default Dashboard;
