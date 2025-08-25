// Color palette for build statuses
export const STATUS_COLORS = {
  success: 'bg-green-600 text-green-200',
  failure: 'bg-red-600 text-red-200',
  'in_progress': 'bg-orange-600 text-orange-200',
  cancelled: 'bg-purple-600 text-purple-200',
};

export const STATUS_LABELS = {
  success: 'Success',
  failure: 'Failure',
  'in_progress': 'In Progress',
  cancelled: 'Cancelled',
};

export const STATUS_CHART_COLORS = {
  success: '#22c55e', // Tailwind green-500
  failure: '#ef4444', // Tailwind red-500
  in_progress: '#f59e42', // Tailwind orange-500
  cancelled: '#a78bfa', // Tailwind purple-400
};
