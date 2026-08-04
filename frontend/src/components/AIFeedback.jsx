import React, { useState } from 'react';
import { Bot, Bug, Lightbulb, Zap, Copy, Check, ShieldAlert } from 'lucide-react';

export const AIFeedback = ({ feedback }) => {
  const [copied, setCopied] = useState(false);

  if (!feedback) return null;

  const { bugs, time_complexity, space_complexity, optimization_tips, corrected_snippet } = feedback;

  const handleCopyCode = () => {
    if (corrected_snippet) {
      navigator.clipboard.writeText(corrected_snippet);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return (
    <div className="flex flex-col gap-4 bg-slate-900/90 p-5 rounded-2xl border border-indigo-900/40 shadow-2xl relative overflow-hidden">
      {/* Glow Ambient Header Background */}
      <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none"></div>

      {/* Card Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-gradient-to-tr from-indigo-600 to-violet-600 text-white shadow-lg">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h4 className="text-base font-bold text-white flex items-center gap-2">
              LangChain AI Code Review
              <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-md bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                Structured Feedback
              </span>
            </h4>
            <p className="text-xs text-slate-400">
              Automated code complexity, logical bug detection & placement tips
            </p>
          </div>
        </div>

        {/* Complexity Badges */}
        <div className="flex items-center gap-2 font-mono text-xs">
          <div className="px-3 py-1 rounded-xl bg-violet-950/60 border border-violet-800/60 text-violet-300">
            Time: <strong className="text-white">{time_complexity || 'O(N)'}</strong>
          </div>
          <div className="px-3 py-1 rounded-xl bg-cyan-950/60 border border-cyan-800/60 text-cyan-300">
            Space: <strong className="text-white">{space_complexity || 'O(1)'}</strong>
          </div>
        </div>
      </div>

      {/* 1. Bugs Section */}
      {bugs && bugs.length > 0 && (
        <div className="p-4 rounded-xl bg-rose-950/20 border border-rose-900/40 space-y-2">
          <h5 className="text-xs font-bold uppercase tracking-wider text-rose-400 flex items-center gap-2">
            <Bug className="w-4 h-4 text-rose-400" />
            Detected Logical Issues / Edge Case Bugs ({bugs.length})
          </h5>
          <ul className="space-y-1.5 pl-6 list-disc text-xs text-rose-200">
            {bugs.map((bug, i) => (
              <li key={i}>{bug}</li>
            ))}
          </ul>
        </div>
      )}

      {/* 2. Optimization Tips Section */}
      {optimization_tips && optimization_tips.length > 0 && (
        <div className="p-4 rounded-xl bg-indigo-950/20 border border-indigo-900/40 space-y-2">
          <h5 className="text-xs font-bold uppercase tracking-wider text-indigo-300 flex items-center gap-2">
            <Lightbulb className="w-4 h-4 text-amber-400" />
            Interview Optimization Tips & Best Practices
          </h5>
          <ul className="space-y-1.5 pl-6 list-disc text-xs text-slate-300">
            {optimization_tips.map((tip, i) => (
              <li key={i}>{tip}</li>
            ))}
          </ul>
        </div>
      )}

      {/* 3. Corrected / Suggested Snippet Section */}
      {corrected_snippet && (
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <h5 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-2">
              <Zap className="w-4 h-4 text-cyan-400" />
              Optimal Code Snippet Reference
            </h5>
            <button
              onClick={handleCopyCode}
              className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors border border-slate-700"
            >
              {copied ? (
                <>
                  <Check className="w-3.5 h-3.5 text-emerald-400" />
                  Copied!
                </>
              ) : (
                <>
                  <Copy className="w-3.5 h-3.5 text-slate-400" />
                  Copy Code
                </>
              )}
            </button>
          </div>

          <pre className="p-4 rounded-xl bg-slate-950 border border-slate-800 font-mono text-xs text-indigo-200 overflow-x-auto leading-relaxed">
            <code>{corrected_snippet}</code>
          </pre>
        </div>
      )}
    </div>
  );
};
