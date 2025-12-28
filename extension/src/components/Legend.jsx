import React from 'react';

const items = [
  { icon: "✋", text: "Compose Email" },
  { icon: "✊", text: "Send Email" },
  { icon: "👍", text: "Next Email" },
  { icon: "👎", text: "Previous Email" },
  { icon: "☝️", text: "Voice Dictation" },
];

export default function Legend() {
  return (
    <div className="legend-grid">
      {items.map((item, index) => (
        <div key={index} className="legend-item">
          <span>{item.icon}</span>
          <span>{item.text}</span>
        </div>
      ))}
    </div>
  );
}