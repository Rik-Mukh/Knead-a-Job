import React, { useState } from 'react';
import { matchService } from '../services/matchService';
import MatchScoreDisplay from '../components/MatchScoreDisplay';

const MatchAnalysis = () => {
  const [jobDescription, setJobDescription] = useState('');
  const [matchResult, setMatchResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);

  const handleAnalyze = async () => {
    if (!jobDescription || !jobDescription.trim()) {
      setError('Please enter a job description to analyze.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await matchService.computeMatchScore(jobDescription);
      setMatchResult(result);
      setShowModal(true);
    } catch (err) {
      setError('Failed to analyze job description. Please try again.');
      console.error('Match analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setJobDescription('');
    setMatchResult(null);
    setError(null);
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      {/* Header */}
      <div style={{ marginBottom: '30px' }}>
        <h1 style={{ 
          font: "normal 500 2.5rem helvetica-neue-lt-pro",
          marginBottom: '8px',
          color: '#1f2937'
        }}>
          Resume Match Analysis
        </h1>
        <p style={{ 
          color: '#6b7280',
          fontSize: '1.1rem',
          lineHeight: '1.5'
        }}>
          Analyze how well your resume matches any job description. Get insights on missing keywords 
          and areas for improvement to increase your chances of landing the job.
        </p>
      </div>

      {/* Input Section */}
      <div style={{
        backgroundColor: '#f9fafb',
        border: '1px solid #e5e7eb',
        borderRadius: '12px',
        padding: '24px',
        marginBottom: '20px'
      }}>
        <div style={{ marginBottom: '20px' }}>
          <label style={{
            display: 'block',
            fontSize: '1.1rem',
            fontWeight: '600',
            color: '#374151',
            marginBottom: '8px'
          }}>
            Job Description
          </label>
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the complete job description here. Include requirements, responsibilities, and preferred qualifications..."
            style={{
              width: '100%',
              minHeight: '200px',
              padding: '12px',
              border: '1px solid #d1d5db',
              borderRadius: '6px',
              fontSize: '1rem',
              lineHeight: '1.5',
              resize: 'vertical',
              fontFamily: 'inherit'
            }}
          />
        </div>

        {/* Action Buttons */}
        <div style={{
          display: 'flex',
          gap: '12px',
          justifyContent: 'flex-end'
        }}>
          <button
            onClick={handleClear}
            disabled={loading}
            style={{
              backgroundColor: '#f3f4f6',
              color: '#374151',
              border: '1px solid #d1d5db',
              borderRadius: '6px',
              padding: '10px 20px',
              fontSize: '1rem',
              fontWeight: '500',
              cursor: loading ? 'not-allowed' : 'pointer',
              opacity: loading ? 0.6 : 1
            }}
          >
            Clear
          </button>
          <button
            onClick={handleAnalyze}
            disabled={loading || !jobDescription.trim()}
            style={{
              backgroundColor: loading ? '#9ca3af' : '#3b82f6',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              padding: '10px 20px',
              fontSize: '1rem',
              fontWeight: '500',
              cursor: loading ? 'not-allowed' : 'pointer',
              transition: 'background-color 0.2s'
            }}
          >
            {loading ? 'Analyzing...' : '📊 Analyze Match Score'}
          </button>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div style={{
          backgroundColor: '#fef2f2',
          border: '1px solid #fecaca',
          borderRadius: '6px',
          padding: '16px',
          marginBottom: '20px',
          color: '#dc2626'
        }}>
          <div style={{ fontWeight: '600', marginBottom: '4px' }}>Error</div>
          <div>{error}</div>
        </div>
      )}

      {/* Quick Results (Inline) */}
      {matchResult && matchResult.success && !showModal && (
        <div style={{
          backgroundColor: '#f0f9ff',
          border: '1px solid #bae6fd',
          borderRadius: '12px',
          padding: '20px',
          marginBottom: '20px'
        }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            marginBottom: '16px'
          }}>
            <h3 style={{ margin: 0, color: '#0c4a6e' }}>Quick Results</h3>
            <button
              onClick={() => setShowModal(true)}
              style={{
                backgroundColor: '#0ea5e9',
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                padding: '8px 16px',
                fontSize: '0.9rem',
                cursor: 'pointer'
              }}
            >
              View Detailed Analysis
            </button>
          </div>
          
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '16px',
            flexWrap: 'wrap'
          }}>
            <div style={{
              fontSize: '2rem',
              fontWeight: 'bold',
              color: matchService.getScoreColor(matchResult.score)
            }}>
              {matchService.formatScoreAsPercentage(matchResult.score)}
            </div>
            <div>
              <div style={{
                fontSize: '1.2rem',
                fontWeight: '600',
                color: matchService.getScoreColor(matchResult.score)
              }}>
                {matchService.getScoreLabel(matchResult.score)}
              </div>
              <div style={{ color: '#64748b', fontSize: '0.9rem' }}>
                {matchResult.missing_keywords.length} missing keywords identified
              </div>
            </div>
          </div>
        </div>
      )}

      {/* How It Works Section */}
      <div style={{
        backgroundColor: '#fefce8',
        border: '1px solid #fde047',
        borderRadius: '12px',
        padding: '20px',
        marginTop: '30px'
      }}>
        <h3 style={{ 
          margin: '0 0 12px 0',
          color: '#a16207',
          fontSize: '1.2rem'
        }}>
          How It Works
        </h3>
        <ul style={{ 
          margin: 0,
          paddingLeft: '20px',
          color: '#a16207',
          lineHeight: '1.6'
        }}>
          <li>Our AI analyzes your resume content and compares it to the job description</li>
          <li>It uses advanced text similarity algorithms to calculate a match score</li>
          <li>Missing keywords are identified using TF-IDF analysis to highlight important terms</li>
          <li>The score helps you understand how well your resume aligns with the job requirements</li>
        </ul>
      </div>

      {/* Tips Section */}
      <div style={{
        backgroundColor: '#f0fdf4',
        border: '1px solid #86efac',
        borderRadius: '12px',
        padding: '20px',
        marginTop: '20px'
      }}>
        <h3 style={{ 
          margin: '0 0 12px 0',
          color: '#166534',
          fontSize: '1.2rem'
        }}>
          Tips for Better Matches
        </h3>
        <ul style={{ 
          margin: 0,
          paddingLeft: '20px',
          color: '#166534',
          lineHeight: '1.6'
        }}>
          <li>Include specific technologies, tools, and skills mentioned in the job description</li>
          <li>Use the same terminology and keywords that appear in the job posting</li>
          <li>Quantify your achievements with numbers and metrics when possible</li>
          <li>Highlight relevant experience that matches the job requirements</li>
          <li>Consider adding a skills section that matches the job's technical requirements</li>
        </ul>
      </div>

      {/* Match Score Display Modal */}
      {showModal && (
        <MatchScoreDisplay
          jobDescription={jobDescription}
          onClose={() => setShowModal(false)}
        />
      )}
    </div>
  );
};

export default MatchAnalysis;
