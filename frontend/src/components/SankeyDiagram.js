import React from 'react';
import { ResponsiveSankey } from '@nivo/sankey';

/**
 * SankeyDiagram Component
 * 
 * Displays a Sankey diagram showing the flow of job applications through different statuses.
 * This visualization helps users understand the distribution and progression of their applications.
 * 
 * @param {Object} props - Component props
 * @param {Array} props.data - The processed data for the Sankey diagram
 * @param {number} props.height - Height of the diagram (default: 400)
 * @returns {JSX.Element} The Sankey diagram component
 */
const SankeyDiagram = ({ data, height = 400 }) => {
  // If no data or empty data, show a message
  if (!data || !data.nodes || data.nodes.length === 0) {
    return (
      <div style={{ 
        height: height, 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center',
        border: '1px solid #e0e0e0',
        borderRadius: '8px',
        backgroundColor: '#f8f9fa'
      }}>
        <p style={{ color: '#666', margin: 0 }}>No data available for Sankey diagram</p>
      </div>
    );
  }

  return (
    <div style={{ height: height, width: '100%' }}>
      <ResponsiveSankey
        data={data}
        margin={{ top: 40, right: 160, bottom: 40, left: 50 }}
        align="justify"
        colors={{ scheme: 'category10' }}
        nodeOpacity={0.8}
        nodeHoverOthersOpacity={0.1}
        nodeThickness={18}
        nodeSpacing={24}
        nodeBorderWidth={0}
        nodeBorderColor={{
          from: 'color',
          modifiers: [['darker', 0.8]]
        }}
        nodeBorderRadius={3}
        linkOpacity={0.5}
        linkHoverOthersOpacity={0.1}
        linkContract={3}
        enableLinkGradient={true}
        labelPosition="outside"
        labelOrientation="vertical"
        labelPadding={16}
        labelTextColor={{
          from: 'color',
          modifiers: [['darker', 1]]
        }}
        legends={[
          {
            anchor: 'bottom-right',
            direction: 'column',
            translateX: 130,
            itemWidth: 100,
            itemHeight: 14,
            itemDirection: 'right-to-left',
            itemsSpacing: 2,
            itemTextColor: '#999',
            symbolSize: 14,
            effects: [
              {
                on: 'hover',
                style: {
                  itemTextColor: '#000'
                }
              }
            ]
          }
        ]}
        animate={true}
        motionConfig="gentle"
      />
    </div>
  );
};

export default SankeyDiagram;
