/**
 * Sankey Data Processor
 * 
 * This utility processes job application data into the format required by the Sankey diagram.
 * It creates nodes and links to show the flow of applications through different statuses.
 */

/**
 * Process job applications data into Sankey diagram format
 * 
 * @param {Array} applications - Array of job application objects
 * @returns {Object} Formatted data for Sankey diagram with nodes and links
 */
export const processApplicationsForSankey = (applications) => {
  if (!applications || applications.length === 0) {
    return { nodes: [], links: [] };
  }

  // Define the flow stages in logical order
  const stages = [
    { id: 'applied', label: 'Applied', color: '#17a2b8' },
    { id: 'interview', label: 'Interview', color: '#ffc107' },
    { id: 'rejected', label: 'Rejected', color: '#dc3545' },
    { id: 'accepted', label: 'Accepted', color: '#28a745' },
    { id: 'withdrawn', label: 'Withdrawn', color: '#6c757d' }
  ];

  // Count applications by status
  const statusCounts = applications.reduce((acc, app) => {
    acc[app.status] = (acc[app.status] || 0) + 1;
    return acc;
  }, {});

  // Calculate counts according to new requirements:
  // 1. Applied = total count of all applications (regardless of current status)
  // 2. Interview = combination of interview, accepted, and rejected statuses
  // 3. Accepted and Rejected stay the same
  // 4. Withdrawn stays the same
  const totalApplications = applications.length;
  const interviewCount = (statusCounts.interview || 0) + (statusCounts.accepted || 0) + (statusCounts.rejected || 0);
  
  // Create adjusted counts for Sankey diagram
  const adjustedCounts = {
    applied: totalApplications,
    interview: interviewCount,
    accepted: statusCounts.accepted || 0,
    rejected: statusCounts.rejected || 0,
    withdrawn: statusCounts.withdrawn || 0
  };

  // Create nodes for each stage that has applications
  const nodes = stages
    .filter(stage => adjustedCounts[stage.id] > 0)
    .map(stage => ({
      id: stage.id,
      label: stage.label,
      color: stage.color
    }));

  // Create links following the logical flow:
  // Applied → Interview or Withdrawn
  // Interview → Accepted or Rejected
  const links = [];
  
  // Flow 1: Applied → Interview (using adjusted count)
  if (adjustedCounts.applied > 0 && adjustedCounts.interview > 0) {
    links.push({
      source: 'applied',
      target: 'interview',
      value: adjustedCounts.interview
    });
  }
  
  // Flow 2: Applied → Withdrawn (for applications that were withdrawn before interview)
  if (adjustedCounts.applied > 0 && adjustedCounts.withdrawn > 0) {
    links.push({
      source: 'applied',
      target: 'withdrawn',
      value: adjustedCounts.withdrawn
    });
  }
  
  // Flow 3: Interview → Accepted
  if (adjustedCounts.interview > 0 && adjustedCounts.accepted > 0) {
    links.push({
      source: 'interview',
      target: 'accepted',
      value: adjustedCounts.accepted
    });
  }
  
  // Flow 4: Interview → Rejected
  if (adjustedCounts.interview > 0 && adjustedCounts.rejected > 0) {
    links.push({
      source: 'interview',
      target: 'rejected',
      value: adjustedCounts.rejected
    });
  }

  return { nodes, links };
};

/**
 * Process applications with company grouping for more detailed Sankey diagram
 * 
 * @param {Array} applications - Array of job application objects
 * @returns {Object} Formatted data for Sankey diagram showing company flows
 */
export const processApplicationsWithCompanies = (applications) => {
  if (!applications || applications.length === 0) {
    return { nodes: [], links: [] };
  }

  // Group applications by company and status
  const companyStatusCounts = applications.reduce((acc, app) => {
    const key = `${app.company_name}-${app.status}`;
    acc[key] = (acc[key] || 0) + 1;
    return acc;
  }, {});

  // Create nodes for companies and statuses
  const nodes = [];
  const links = [];
  const companyNodes = new Set();
  const statusNodes = new Set();

  // Process each application
  applications.forEach(app => {
    const companyId = `company-${app.company_name}`;
    const statusId = `status-${app.status}`;
    
    // Add company node if not already added
    if (!companyNodes.has(companyId)) {
      nodes.push({
        id: companyId,
        label: app.company_name,
        color: '#6c757d'
      });
      companyNodes.add(companyId);
    }

    // Add status node if not already added
    if (!statusNodes.has(statusId)) {
      const statusColors = {
        'applied': '#17a2b8',
        'interview': '#ffc107',
        'rejected': '#dc3545',
        'accepted': '#28a745',
        'withdrawn': '#6c757d'
      };
      
      nodes.push({
        id: statusId,
        label: app.status.charAt(0).toUpperCase() + app.status.slice(1),
        color: statusColors[app.status] || '#6c757d'
      });
      statusNodes.add(statusId);
    }

    // Add link from company to status
    links.push({
      source: companyId,
      target: statusId,
      value: 1
    });
  });

  return { nodes, links };
};
