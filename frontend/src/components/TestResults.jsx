import React from 'react';
import { CheckCircle2, XCircle, Clock, AlertTriangle, Cpu } from 'lucide-react';

export const TestResults = ({ execution, topicScoreUpdate }) => {
  if (!execution) return null;

  const { passed_all, passed_count, total_tests, avg_runtime_ms, results } = execution;

  return (
    <div className="flex flex-col gap-4 bg-slate-900/90 p-5 rounded-2xl border border-slate-800 shadow-xl">
      {/* Execution Summary Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-xl bg-slate-950/80 border border-slate-800">
        <div className="flex items-center gap-3">
          {passed_all ? (
            <div className="p-2.5 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <CheckCircle2 className="w-6 h-6" />
            </div>
          ) : (
            <div className="p-2.5 rounded-xl bg-rose-500/10 text-rose-400 border border-rose-500/20">
              <XCircle className="w-6 h-6" />
            </div>
          )}
          <div>
            <h4 className="text-base font-bold text-white flex items-center gap-2">
              {passed_all ? "All Test Cases Passed!" : "Submission Failed"}
              <span className={`text-xs px-2.5 py-0.5 rounded-full font-semibold ${
                passed_all ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
              }`}>
                {passed_count} / {total_tests} Passed
              </span>
            </h4>
            <p className="text-xs text-slate-400 mt-0.5">
              {passed_all
                ? "Great job! Your solution produces correct outputs across all test vectors."
                : "One or more test cases returned incorrect outputs or errors."}
            </p>
          </div>
        </div>

        {/* Runtime Metric & Topic Score Update Pill */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-slate-900 border border-slate-800 text-xs font-mono text-cyan-300">
            <Clock className="w-3.5 h-3.5 text-cyan-400" />
            <span>Avg Runtime: <strong>{avg_runtime_ms} ms</strong></span>
          </div>

          {topicScoreUpdate && (
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-indigo-950/60 border border-indigo-800/80 text-xs font-mono text-indigo-300">
              <Cpu className="w-3.5 h-3.5 text-indigo-400" />
              <span>
                EMA Mastery: <strong>{Math.round(topicScoreUpdate.new_score * 100)}%</strong>
              </span>
            </div>
          )}
        </div>
      </div>

      {/* Test Case Detail Accordion Cards */}
      <div className="space-y-3">
        <h5 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center gap-2">
          Test Case Breakdown
        </h5>

        <div className="grid grid-cols-1 gap-3">
          {results && results.map((tc, idx) => (
            <div
              key={idx}
              className={`p-3.5 rounded-xl border transition-all ${
                tc.passed
                  ? 'bg-slate-950/40 border-slate-800'
                  : 'bg-rose-950/20 border-rose-900/50'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2 text-xs font-semibold">
                  {tc.passed ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                  ) : (
                    <XCircle className="w-4 h-4 text-rose-400" />
                  )}
                  <span className={tc.passed ? "text-slate-200" : "text-rose-300"}>
                    Test Case #{tc.test_case}
                  </span>
                </div>
                <span className="text-[11px] font-mono text-slate-500">
                  {tc.execution_time_ms} ms
                </span>
              </div>

              {/* Input / Expected / Actual Grid */}
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-2 text-xs font-mono">
                <div className="p-2 rounded-lg bg-slate-900/90 border border-slate-800/80">
                  <span className="text-[10px] text-slate-400 uppercase block mb-1">Input</span>
                  <div className="text-slate-200 font-semibold whitespace-pre-wrap">{tc.input || "(empty)"}</div>
                </div>

                <div className="p-2 rounded-lg bg-slate-900/90 border border-slate-800/80">
                  <span className="text-[10px] text-slate-400 uppercase block mb-1">Expected</span>
                  <div className="text-emerald-400 font-semibold whitespace-pre-wrap">{tc.expected}</div>
                </div>

                <div className="p-2 rounded-lg bg-slate-900/90 border border-slate-800/80">
                  <span className="text-[10px] text-slate-400 uppercase block mb-1">Output</span>
                  <div className={`font-semibold whitespace-pre-wrap ${tc.passed ? "text-slate-200" : "text-rose-400"}`}>
                    {tc.actual || "(no output)"}
                  </div>
                </div>
              </div>

              {tc.error && (
                <div className="mt-2.5 p-2 rounded-lg bg-rose-950/40 border border-rose-900/60 text-xs text-rose-300 flex items-start gap-2">
                  <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                  <span className="font-mono">{tc.error}</span>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
