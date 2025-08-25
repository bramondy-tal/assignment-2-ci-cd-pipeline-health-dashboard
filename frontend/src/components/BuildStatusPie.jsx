import React from 'react';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { STATUS_CHART_COLORS, STATUS_LABELS } from '../constants';

export default function BuildStatusPie({ data }) {
  // data: [{ status: 'success', value: 10 }, ...]
  return (
    <div className="w-full h-64">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="status"
            cx="50%"
            cy="50%"
            outerRadius={80}
            label={({ status }) => STATUS_LABELS[status]}
          >
            {data.map((entry, idx) => (
              <Cell key={`cell-${idx}`} fill={STATUS_CHART_COLORS[entry.status] || '#8884d8'} />
            ))}
          </Pie>
          <Tooltip contentStyle={{ backgroundColor: '#0b1220', border: '1px solid #1f2937', color: '#e5e7eb' }} formatter={(v, n, p) => [v, STATUS_LABELS[p.payload.status] || p.payload.status]} />
          <Legend wrapperStyle={{ color: '#e5e7eb' }} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
