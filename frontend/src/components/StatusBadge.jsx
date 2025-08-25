import React from 'react';
import { STATUS_COLORS, STATUS_LABELS } from '../constants';

export default function StatusBadge({ status }) {
  const color = STATUS_COLORS[status] || 'bg-gray-700 text-gray-200';
  return (
    <span className={`px-2 py-1 rounded text-xs font-semibold ${color}`}>{STATUS_LABELS[status] || status}</span>
  );
}
