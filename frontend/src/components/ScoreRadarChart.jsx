import React from 'react';
import {
  Radar,
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell
} from 'recharts';
import { Award } from 'lucide-react';

const TOPIC_COLORS = {
  arrays: '#3b82f6',   // Blue
  strings: '#06b6d4',  // Cyan
  dp: '#8b5cf6',       // Purple
  graphs: '#ec4899',   // Pink
  trees: '#10b981'     // Emerald
};

export const ScoreRadarChart = ({ scores }) => {
  if (!scores || scores.length === 0) return null;

  // Format score to 0-100 percentage scale for display
  const chartData = scores.map((s) => ({
    topic: s.topic.toUpperCase(),
    raw_topic: s.topic,
    scorePercent: Math.round((s.score || 0.5) * 100),
    scoreFloat: s.score || 0.5
  }));

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      
      {/* 1. Radar Chart Panel */}
      <div className="bg-slate-900/90 p-5 rounded-2xl border border-slate-800 shadow-xl flex flex-col items-center">
        <div className="w-full flex items-center justify-between border-b border-slate-800 pb-3 mb-2">
          <h4 className="text-sm font-bold text-white flex items-center gap-2">
            <Award className="w-4 h-4 text-indigo-400" />
            Skill Mastery Radar
          </h4>
          <span className="text-xs text-slate-400 font-mono">0 - 100% Scale</span>
        </div>

        <div className="w-full h-[280px]">
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart cx="50%" cy="50%" outerRadius="75%" data={chartData}>
              <PolarGrid stroke="#334155" />
              <PolarAngleAxis dataKey="topic" stroke="#94a3b8" tick={{ fill: '#cbd5e1', fontSize: 11, fontWeight: 600 }} />
              <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#475569" tick={{ fill: '#64748b', fontSize: 10 }} />
              <Radar
                name="Topic Mastery"
                dataKey="scorePercent"
                stroke="#6366f1"
                fill="#6366f1"
                fillOpacity={0.4}
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* 2. Bar Chart Breakdown Panel */}
      <div className="bg-slate-900/90 p-5 rounded-2xl border border-slate-800 shadow-xl flex flex-col">
        <div className="w-full flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
          <h4 className="text-sm font-bold text-white flex items-center gap-2">
            Topic Breakdown (EMA Scores)
          </h4>
          <span className="text-xs text-slate-400 font-mono">Alpha = 0.3</span>
        </div>

        <div className="w-full h-[260px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <XAxis dataKey="topic" stroke="#64748b" tick={{ fill: '#94a3b8', fontSize: 11 }} />
              <YAxis domain={[0, 100]} stroke="#64748b" tick={{ fill: '#94a3b8', fontSize: 11 }} />
              <Tooltip
                contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '12px', color: '#f8fafc' }}
                formatter={(val) => [`${val}%`, 'Mastery Score']}
              />
              <Bar dataKey="scorePercent" radius={[6, 6, 0, 0]}>
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={TOPIC_COLORS[entry.raw_topic] || '#6366f1'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

    </div>
  );
};
