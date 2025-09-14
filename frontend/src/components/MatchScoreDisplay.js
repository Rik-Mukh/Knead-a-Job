import React, { useState } from 'react';
import { matchService } from '../services/matchService';

const MatchScoreDisplay = ({ jobDescription, onClose }) => {
  const [matchResult, setMatchResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

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
    } catch (err) {
      setError('Failed to analyze job description. Please try again.');
      console.error('Match analysis error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 0.8) return '#10b981'; // emerald-500
    if (score >= 0.6) return '#3b82f6'; // blue-500
    if (score >= 0.4) return '#f59e0b'; // amber-500
    if (score >= 0.2) return '#ef4444'; // red-500
    return '#6b7280'; // gray-500
  };

  const getScoreLabel = (score) => {
    if (score >= 0.8) return 'Excellent Match';
    if (score >= 0.6) return 'Good Match';
    if (score >= 0.4) return 'Moderate Match';
    if (score >= 0.2) return 'Poor Match';
    return 'Very Poor Match';
  };

  return (
    <div className="match-score-display" style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
      padding: '20px'
    }}>
      <div style={{
        backgroundColor: 'white',
        borderRadius: '12px',
        padding: '24px',
        maxWidth: '700px',
        width: '100%',
        maxHeight: '80vh',
        overflowY: 'auto',
        boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)'
      }}>
        {/* Header */}
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '20px',
          paddingBottom: '16px',
          borderBottom: '1px solid #e5e7eb'
        }}>
          <h2 style={{ margin: 0, fontSize: '1.5rem', fontWeight: '600' }}>
            Resume Match Analysis
          </h2>
          <button
            onClick={onClose}
            style={{
              background: 'none',
              border: 'none',
              fontSize: '1.5rem',
              cursor: 'pointer',
              color: '#6b7280',
              padding: '4px'
            }}
          >
            ×
          </button>
        </div>

        {/* Job Description Preview */}
        <div style={{ marginBottom: '20px' }}>
          <h3 style={{ fontSize: '1.1rem', marginBottom: '8px', color: '#374151' }}>
            Job Description Preview:
          </h3>
          <div style={{
            backgroundColor: '#f9fafb',
            border: '1px solid #e5e7eb',
            borderRadius: '6px',
            padding: '12px',
            fontSize: '0.9rem',
            color: '#6b7280',
            maxHeight: '120px',
            overflowY: 'auto'
          }}>
            {jobDescription ? 
              (jobDescription.length > 300 ? `${jobDescription.substring(0, 300)}...` : jobDescription) :
              'No job description provided'
            }
          </div>
        </div>

        {/* Analyze Button */}
        {!matchResult && (
          <div style={{ textAlign: 'center', marginBottom: '20px' }}>
            <button
              onClick={handleAnalyze}
              disabled={loading || !jobDescription?.trim()}
              style={{
                backgroundColor: loading ? '#9ca3af' : '#3b82f6',
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                padding: '12px 24px',
                fontSize: '1rem',
                fontWeight: '500',
                cursor: loading ? 'not-allowed' : 'pointer',
                transition: 'background-color 0.2s'
              }}
            >
              {loading ? 'Analyzing...' : 'Analyze Match Score'}
            </button>
          </div>
        )}

        {/* Error Display */}
        {error && (
          <div style={{
            backgroundColor: '#fef2f2',
            border: '1px solid #fecaca',
            borderRadius: '6px',
            padding: '12px',
            marginBottom: '20px',
            color: '#dc2626'
          }}>
            {error}
          </div>
        )}

        {/* Match Results */}
        {matchResult && matchResult.success && (
          <div>
            {/* Overall Score Display */}
            <div style={{
              textAlign: 'center',
              marginBottom: '24px',
              padding: '20px',
              backgroundColor: '#f9fafb',
              borderRadius: '8px',
              border: '1px solid #e5e7eb'
            }}>
              <div style={{
                fontSize: '3rem',
                fontWeight: 'bold',
                color: getScoreColor(matchResult.score),
                marginBottom: '8px'
              }}>
                {matchService.formatScoreAsPercentage(matchResult.score)}
              </div>
              <div style={{
                fontSize: '1.2rem',
                fontWeight: '600',
                color: getScoreColor(matchResult.score),
                marginBottom: '4px'
              }}>
                {getScoreLabel(matchResult.score)}
              </div>
              <div style={{ color: '#6b7280', fontSize: '0.9rem' }}>
                {matchService.getScoreDescription(matchResult.score, matchResult.missing_keywords, matchResult.skills_analysis)}
              </div>
            </div>

            {/* Skills Analysis Section */}
            {matchResult.skills_analysis && matchResult.skills_analysis.total_skills_mentioned > 0 && (
              <div style={{
                backgroundColor: '#f0f9ff',
                border: '1px solid #bae6fd',
                borderRadius: '8px',
                padding: '20px',
                marginBottom: '20px'
              }}>
                <h3 style={{ fontSize: '1.2rem', marginBottom: '16px', color: '#0c4a6e' }}>
                  Skills Analysis
                </h3>
                
                {/* Skills Coverage */}
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  marginBottom: '16px'
                }}>
                  <span style={{ fontWeight: '500', color: '#0c4a6e' }}>Skills Coverage:</span>
                  <span style={{
                    fontSize: '1.5rem',
                    fontWeight: 'bold',
                    color: matchService.getSkillsCoverageColor(matchResult.skills_analysis)
                  }}>
                    {matchService.formatSkillsCoverage(matchResult.skills_analysis)}
                  </span>
                </div>

                {/* Skills Found */}
                {matchResult.skills_analysis.skills_found && matchResult.skills_analysis.skills_found.length > 0 && (
                  <div style={{ marginBottom: '12px' }}>
                    <div style={{ fontSize: '0.9rem', fontWeight: '500', color: '#0c4a6e', marginBottom: '6px' }}>
                      Skills You Have ({matchResult.skills_analysis.skills_found.length}):
                    </div>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                      {matchResult.skills_analysis.skills_found.map((skill, index) => (
                        <span
                          key={index}
                          style={{
                            backgroundColor: '#dcfce7',
                            color: '#166534',
                            padding: '4px 8px',
                            borderRadius: '4px',
                            fontSize: '0.8rem',
                            fontWeight: '500'
                          }}
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Skills Missing */}
                {matchResult.skills_analysis.skills_missing && matchResult.skills_analysis.skills_missing.length > 0 && (
                  <div>
                    <div style={{ fontSize: '0.9rem', fontWeight: '500', color: '#0c4a6e', marginBottom: '6px' }}>
                      Skills You're Missing ({matchResult.skills_analysis.skills_missing.length}):
                    </div>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
                      {matchResult.skills_analysis.skills_missing.map((skill, index) => (
                        <span
                          key={index}
                          style={{
                            backgroundColor: '#fef3c7',
                            color: '#92400e',
                            padding: '4px 8px',
                            borderRadius: '4px',
                            fontSize: '0.8rem',
                            fontWeight: '500'
                          }}
                        >
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Missing Keywords */}
            {matchResult.missing_keywords && matchResult.missing_keywords.length > 0 && (
              <div style={{ marginBottom: '20px' }}>
                <h3 style={{ fontSize: '1.1rem', marginBottom: '12px', color: '#374151' }}>
                  Keywords to Consider Adding:
                </h3>
                <div style={{
                  display: 'flex',
                  flexWrap: 'wrap',
                  gap: '8px'
                }}>
                  {matchResult.missing_keywords.slice(0, 10).map((keyword, index) => (
                    <span
                      key={index}
                      style={{
                        backgroundColor: '#fef3c7',
                        color: '#92400e',
                        padding: '4px 8px',
                        borderRadius: '4px',
                        fontSize: '0.85rem',
                        fontWeight: '500'
                      }}
                    >
                      {keyword}
                    </span>
                  ))}
                  {matchResult.missing_keywords.length > 10 && (
                    <span style={{
                      backgroundColor: '#e5e7eb',
                      color: '#6b7280',
                      padding: '4px 8px',
                      borderRadius: '4px',
                      fontSize: '0.85rem'
                    }}>
                      +{matchResult.missing_keywords.length - 10} more
                    </span>
                  )}
                </div>
              </div>
            )}

            {/* Action Buttons */}
            <div style={{
              display: 'flex',
              gap: '12px',
              justifyContent: 'flex-end',
              marginTop: '24px',
              paddingTop: '16px',
              borderTop: '1px solid #e5e7eb'
            }}>
              <button
                onClick={() => setMatchResult(null)}
                style={{
                  backgroundColor: '#f3f4f6',
                  color: '#374151',
                  border: '1px solid #d1d5db',
                  borderRadius: '6px',
                  padding: '8px 16px',
                  fontSize: '0.9rem',
                  cursor: 'pointer'
                }}
              >
                Analyze Again
              </button>
              <button
                onClick={onClose}
                style={{
                  backgroundColor: '#3b82f6',
                  color: 'white',
                  border: 'none',
                  borderRadius: '6px',
                  padding: '8px 16px',
                  fontSize: '0.9rem',
                  cursor: 'pointer'
                }}
              >
                Close
              </button>
            </div>
          </div>
        )}

        {/* Match Error */}
        {matchResult && !matchResult.success && (
          <div style={{
            backgroundColor: '#fef2f2',
            border: '1px solid #fecaca',
            borderRadius: '6px',
            padding: '16px',
            textAlign: 'center'
          }}>
            <div style={{ color: '#dc2626', marginBottom: '12px' }}>
              <strong>Analysis Failed</strong>
            </div>
            <div style={{ color: '#6b7280', fontSize: '0.9rem', marginBottom: '16px' }}>
              {matchResult.error || 'Unable to analyze the job description. Please try again.'}
            </div>
            <button
              onClick={() => setMatchResult(null)}
              style={{
                backgroundColor: '#3b82f6',
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                padding: '8px 16px',
                fontSize: '0.9rem',
                cursor: 'pointer'
              }}
            >
              Try Again
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default MatchScoreDisplay;
