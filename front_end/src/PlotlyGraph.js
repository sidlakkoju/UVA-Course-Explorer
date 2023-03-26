import React from 'react';

const PlotlyGraph = ({ src, width, height }) => {
  return (
    <iframe
      src={src}
      style={{
        width: width || '100%',
        height: height || '100%',
        border: 'none',
      }}
      title="Plotly Graph"
    ></iframe>
  );
};

export default PlotlyGraph;