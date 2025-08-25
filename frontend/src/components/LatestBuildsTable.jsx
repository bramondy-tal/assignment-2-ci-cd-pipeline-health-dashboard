import React from 'react';
import StatusBadge from './StatusBadge';

export default function LatestBuildsTable({ builds }) {
  return (
    <div className="overflow-x-auto rounded-xl border border-gray-800 bg-gray-900">
      <table className="min-w-full text-sm text-gray-100">
        <thead className="bg-gray-900 sticky top-0 z-10">
          <tr>
            <th className="px-4 py-2 text-left text-gray-300 font-medium">Repo</th>
            <th className="px-4 py-2 text-left text-gray-300 font-medium">Branch</th>
            <th className="px-4 py-2 text-left text-gray-300 font-medium">Status</th>
            <th className="px-4 py-2 text-left text-gray-300 font-medium">Duration (s)</th>
            <th className="px-4 py-2 text-left text-gray-300 font-medium">GitHub Run</th>
          </tr>
        </thead>
        <tbody>
          {builds.map((b, i) => (
            <tr key={b.github_run_id || i} className={i % 2 === 0 ? 'bg-gray-900' : 'bg-gray-900/60 hover:bg-gray-800/60'}>
              <td className="px-4 py-2 border-t border-gray-800">{b.repo}</td>
              <td className="px-4 py-2 border-t border-gray-800">{b.branch}</td>
              <td className="px-4 py-2 border-t border-gray-800"><StatusBadge status={b.status} /></td>
              <td className="px-4 py-2 border-t border-gray-800">{b.duration}</td>
              <td className="px-4 py-2 border-t border-gray-800">
                <a href={`https://github.com/${b.repo}/actions/runs/${b.github_run_id}`} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:text-blue-300">View</a>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
