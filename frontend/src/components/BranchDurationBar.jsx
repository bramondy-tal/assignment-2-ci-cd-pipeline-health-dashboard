import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { STATUS_CHART_COLORS } from '../constants';

export default function BranchDurationBar({ data, onBarClick }) {
  // data: [{ branch: 'main', avg_duration: 120, status: 'success' }, ...]
  return (
    <div className="w-full h-64">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 30 }}>
          <XAxis dataKey="branch" stroke="#d1d5db" tick={{ fill: '#d1d5db' }} />
          <YAxis stroke="#d1d5db" tick={{ fill: '#d1d5db' }} />
          <Tooltip contentStyle={{ backgroundColor: '#0b1220', border: '1px solid #1f2937', color: '#e5e7eb' }} />
          <Bar dataKey="avg_duration" onClick={onBarClick}>
            {data.map((entry, idx) => (
              <Cell key={`cell-${idx}`} fill={STATUS_CHART_COLORS[entry.status] || '#8884d8'} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
