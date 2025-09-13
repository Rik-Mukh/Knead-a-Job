import React, { useState, useEffect } from "react";
import Timeline from "../components/Timeline"; 
import { mockApplications, mockResume } from "./TestData";
import "./Dashboard.css";

const STATUS_MAP = {
  offer: { label: "Offer", color: "#E1FFCD" },
  applied: { label: "Applied", color: "#EFEFEF" },
  interview: { label: "Interview", color: "#C8F1FF" },
  rejected: { label: "Rejected", color: "#FFCDCD" },
  withdrawn: { label: "Withdrawn", color: "#6c757d" },
};

const StatusBadge = ({ status }) => {
  if (!status) return null;
  const key = status.toLowerCase();
  const s = STATUS_MAP[key] || { label: status, color: "#6c757d" };

  return (
    <span className="status-badge" style={{ backgroundColor: s.color }}>
      <span className="status-dot" style={{ backgroundColor: "#fff" }} />
      <span>{s.label}</span>
    </span>
  );
};

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
  const [selectedApp, setSelectedApp] = useState(null);

  useEffect(() => {
    // ✅ Using mock data instead of API
    setRecentApplications(mockApplications);
    setDefaultResume(mockResume);
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div className="dashboard-wrap">
        <h2>Dashboard</h2>
        <p>Loading...</p>
      </div>
    );
  }

  return (
    <div className="dashboard-wrap">
      {/* Hero */}
      <div className="dashboard-hero">
        <div className="hero-date">{formatDate(new Date())}</div>
        <h1 className="hero-title">So far, you’ve applied to...</h1>
      </div>

      {/* Applications Table */}
      <div className="table-card">
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
                <td
                  colSpan="5"
                  style={{ textAlign: "center", padding: "24px", color: "#777" }}
                >
                  No applications yet.
                </td>
              </tr>
            )}
            {recentApplications.map((app) => (
              <tr
                key={app.id || app.company_name + app.applied_date}
                onClick={() => setSelectedApp(app)}
                style={{ cursor: "pointer" }}
              >
                <td className="company-cell">{app.company_name}</td>
                <td>{app.position}</td>
                <td>{formatDate(app.applied_date)}</td>
                <td>
                  <StatusBadge status={app.status} />
                </td>
                <td>
                  <a
                    className="resume-link"
                    href={app.resume_url || "#"}
                    target="_blank"
                    rel="noopener noreferrer"
                    onClick={(e) => e.stopPropagation()} // ✅ prevents row click
                  >
                    {app.resume_file || "Resume.pdf"}
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Default Resume card (optional) */}
      {defaultResume && (
        <div style={{ marginTop: "24px" }}>
          <div className="table-card">
            <h4 style={{ marginBottom: "8px" }}>{defaultResume.title}</h4>
            <p style={{ margin: "0 0 8px 0", color: "#666", fontSize: "14px" }}>
              Uploaded: {formatDate(defaultResume.created_at)}
            </p>
            <button
              className="btn btn-primary"
              style={{ fontSize: "14px" }}
              onClick={() => window.open(defaultResume.file_url, "_blank")}
            >
              Download Resume
            </button>
          </div>
        </div>
      )}

      {/* ✅ Timeline popup */}
      <Timeline
        isOpen={!!selectedApp}
        onClose={() => setSelectedApp(null)}
        application={selectedApp}
      />
    </div>
  );
};

export default Dashboard;
