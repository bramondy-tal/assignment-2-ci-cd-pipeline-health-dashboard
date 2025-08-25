import React from 'react';

export default function Card({ title, value, icon, color }) {
  return (
    <div className={`rounded-2xl p-5 flex flex-col items-center text-white border border-white/10 backdrop-blur-xl ${color || 'bg-white/5'}`}>
      {icon && (
        <div className="mb-3 text-2xl drop-shadow-sm w-12 h-12 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-500 grid place-items-center">
          {icon}
        </div>
      )}
      <div className="text-gray-200/80 text-sm mb-1">{title}</div>
      <div className="text-3xl font-extrabold tracking-tight">{value}</div>
    </div>
  );
}
