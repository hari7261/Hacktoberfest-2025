// Displays clickable organ info
import React from 'react';
export default function OrganCard({ organ, onClick }) {
  return <div onClick={() => onClick(organ)}>{organ.name}</div>;
}
