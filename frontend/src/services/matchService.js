/**
 * Match Service
 * 
 * This module provides API functions for job description matching functionality.
 * It handles all HTTP requests to the Django backend for match scoring.
 */

import axios from 'axios';

// Base URL for match API endpoints
const API_BASE_URL = 'http://127.0.0.1:8000/api/ai/';

/**
 * Match Service
 * 
 * Object containing methods for all match API operations.
 * Each method handles HTTP requests to the Django backend.
 */
export const matchService = {
  /**
   * Compute match score between user's resume and job description
   * 
   * @param {string} jobDescription - The job description text to match against
   * @returns {Promise<Object>} Object containing match score and missing keywords
   * @returns {Promise<number>} score - Match score between 0 and 1
   * @returns {Promise<Array<string>>} missing_keywords - Array of missing keywords from the job description
   * @returns {Promise<Object>} skills_analysis - Skills analysis object with found/missing skills
   */
  async computeMatchScore(jobDescription) {
    try {
      if (!jobDescription || !jobDescription.trim()) {
        throw new Error('Job description is required');
      }

      const response = await axios.post(`${API_BASE_URL}match/`, {
        job_description: jobDescription.trim()
      });

      return {
        score: response.data.score,
        missing_keywords: response.data.missing_keywords || [],
        skills_analysis: response.data.skills_analysis || {},
        success: true
      };
    } catch (error) {
      console.error("Error computing match score:", error);
      
      // Return a default response structure even on error
      return {
        score: 0,
        missing_keywords: [],
        skills_analysis: {
          skills_found: [],
          skills_missing: [],
          skills_coverage: 0.0,
          total_skills_mentioned: 0
        },
        success: false,
        error: error.response?.data?.detail || error.message || 'Failed to compute match score'
      };
    }
  },

  /**
   * Format match score as percentage
   * 
   * @param {number} score - Match score between 0 and 1
   * @returns {string} Formatted percentage string
   */
  formatScoreAsPercentage(score) {
    if (typeof score !== 'number' || isNaN(score)) {
      return '0%';
    }
    return `${Math.round(score * 100)}%`;
  },

  /**
   * Get match score color based on score value
   * 
   * @param {number} score - Match score between 0 and 1
   * @returns {string} CSS color class or color value
   */
  getScoreColor(score) {
    if (typeof score !== 'number' || isNaN(score)) {
      return '#6b7280'; // gray-500
    }
    
    if (score >= 0.8) {
      return '#10b981'; // emerald-500 - excellent match
    } else if (score >= 0.6) {
      return '#3b82f6'; // blue-500 - good match
    } else if (score >= 0.4) {
      return '#f59e0b'; // amber-500 - moderate match
    } else if (score >= 0.2) {
      return '#ef4444'; // red-500 - poor match
    } else {
      return '#6b7280'; // gray-500 - very poor match
    }
  },

  /**
   * Get match score label based on score value
   * 
   * @param {number} score - Match score between 0 and 1
   * @returns {string} Human-readable match label
   */
  getScoreLabel(score) {
    if (typeof score !== 'number' || isNaN(score)) {
      return 'Unknown';
    }
    
    if (score >= 0.8) {
      return 'Excellent Match';
    } else if (score >= 0.6) {
      return 'Good Match';
    } else if (score >= 0.4) {
      return 'Moderate Match';
    } else if (score >= 0.2) {
      return 'Poor Match';
    } else {
      return 'Very Poor Match';
    }
  },

  /**
   * Get match score description with actionable insights
   * 
   * @param {number} score - Match score between 0 and 1
   * @param {Array<string>} missingKeywords - Array of missing keywords
   * @param {Object} skillsAnalysis - Skills analysis object
   * @returns {string} Detailed description of the match
   */
  getScoreDescription(score, missingKeywords = [], skillsAnalysis = {}) {
    if (typeof score !== 'number' || isNaN(score)) {
      return 'Unable to analyze match score.';
    }

    const percentage = Math.round(score * 100);
    const label = this.getScoreLabel(score);
    
    let description = `Your resume has a ${percentage}% match with this job description (${label}).`;
    
    // Add skills analysis if available
    if (skillsAnalysis && skillsAnalysis.total_skills_mentioned > 0) {
      const skillsCoverage = Math.round(skillsAnalysis.skills_coverage * 100);
      description += ` You have ${skillsCoverage}% skills coverage (${skillsAnalysis.skills_found.length}/${skillsAnalysis.total_skills_mentioned} required skills).`;
    }
    
    if (missingKeywords.length > 0) {
      description += ` Consider adding these keywords to improve your match: ${missingKeywords.slice(0, 5).join(', ')}`;
      if (missingKeywords.length > 5) {
        description += ` and ${missingKeywords.length - 5} more.`;
      }
    }
    
    return description;
  },

  /**
   * Format skills coverage as percentage
   * 
   * @param {Object} skillsAnalysis - Skills analysis object
   * @returns {string} Formatted skills coverage percentage
   */
  formatSkillsCoverage(skillsAnalysis) {
    if (!skillsAnalysis || typeof skillsAnalysis.skills_coverage !== 'number') {
      return '0%';
    }
    return `${Math.round(skillsAnalysis.skills_coverage * 100)}%`;
  },

  /**
   * Get skills coverage color based on coverage value
   * 
   * @param {Object} skillsAnalysis - Skills analysis object
   * @returns {string} CSS color value
   */
  getSkillsCoverageColor(skillsAnalysis) {
    if (!skillsAnalysis || typeof skillsAnalysis.skills_coverage !== 'number') {
      return '#6b7280'; // gray-500
    }
    
    const coverage = skillsAnalysis.skills_coverage;
    if (coverage >= 0.8) {
      return '#10b981'; // emerald-500 - excellent coverage
    } else if (coverage >= 0.6) {
      return '#3b82f6'; // blue-500 - good coverage
    } else if (coverage >= 0.4) {
      return '#f59e0b'; // amber-500 - moderate coverage
    } else if (coverage >= 0.2) {
      return '#ef4444'; // red-500 - poor coverage
    } else {
      return '#6b7280'; // gray-500 - very poor coverage
    }
  }
};
