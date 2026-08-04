import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { fetchDashboardData, fetchNextQuestion } from '../services/api';
import { ScoreRadarChart } from '../components/ScoreRadarChart';
import { AIFeedback } from '../components/AIFeedback';
import {
  Sparkles,
  Award,
  CheckCircle2,
  XCircle,
  Clock,
  Code2,
  TrendingUp,
  Cpu,
  ArrowRight,
  BookOpen
} from 'lucide-react';

export const DashboardPage = () => {
  const [dashboard, setDashboard] = useState(null);
  const [recommendation, setRecommendation] = useState(null);
  const [selectedSubmission, setSelectedSubmission] = useState(null);
  const [loading, setLoading] = useState(true);

  const navigate = useNavigate();

  useEffect(() => {
    const loadDashboard = async () => {
      setLoading(true);
      try {
        const data = await fetchDashboardData();
        setDashboard(data);

        // Fetch recommendation info
        const rec = await fetchNextQuestion();
        setRecommendation(rec);
      } catch (err) {
        console.error("Failed to load dashboard data:", err);
      } finally {
        setLoading(false);
      }
    };
    loadDashboard();
  }, []);

  const handleStartRecommendation = () => {
    if (recommendation && recommendation.question) {
      navigate(`/practice/${recommendation.question.id}`, { state: { recommendation } });
    } else {
      navigate('/questions');
    }
  };

  if (loading) {
    return (
      <div className="py-20 flex justify-center items-center">
        <div className="w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  const stats = dashboard?.stats || {};
  const scores = dashboard?.scores || [];
  const submissions = dashboard?.recent_submissions || [];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      {/* 1. Adaptive Recommendation Hero Card */}
      {recommendation && (
        <div className="bg-gradient-to-r from-violet-950 via-indigo-950 to-slate-900 p-6 rounded-3xl border border-violet-800/60 shadow-2xl relative overflow-hidden flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="absolute top-0 right-0 w-80 h-80 bg-violet-600/10 rounded-full blur-3xl pointer-events-none"></div>

          <div className="space-y-2 max-w-2xl">
            <div className="flex items-center gap-2">
              <span className="text-[11px] font-extrabold uppercase tracking-wider px-3 py-1 rounded-full bg-violet-500/20 text-cyan-300 border border-violet-500/30 flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-cyan-300 animate-pulse" />
                Adaptive AI Recommendation
              </span>
              <span className="text-xs font-mono text-slate-400 capitalize">
                Focus: <strong>{recommendation.target_topic}</strong>
              </span>
            </div>

            <h2 className="text-2xl font-black text-white tracking-tight">
              Recommended: {recommendation.question?.title}
            </h2>

            <p className="text-xs text-slate-300 leading-relaxed">
              {recommendation.reason}
            </p>
          </div>

          <button
            onClick={handleStartRecommendation}
            className="px-6 py-3 rounded-2xl bg-gradient-to-r from-cyan-500 via-indigo-500 to-violet-600 hover:from-cyan-400 hover:to-violet-500 text-white font-bold text-xs shadow-lg shadow-indigo-600/30 transition-all flex items-center justify-center gap-2 shrink-0 border border-cyan-400/30"
          >
            Solve Recommended Problem
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* 2. Key Metrics Summary Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        <div className="bg-slate-900/90 p-5 rounded-2xl border border-slate-800 shadow-xl flex items-center gap-4">
          <div className="p-3 rounded-xl bg-indigo-600/20 text-indigo-400 border border-indigo-500/30">
            <TrendingUp className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs font-semibold text-slate-400 uppercase">Overall Mastery</span>
            <div className="text-2xl font-black text-white mt-0.5">{stats.overall_mastery || 50}%</div>
          </div>
        </div>

        <div className="bg-slate-900/90 p-5 rounded-2xl border border-slate-800 shadow-xl flex items-center gap-4">
          <div className="p-3 rounded-xl bg-emerald-600/20 text-emerald-400 border border-emerald-500/30">
            <CheckCircle2 className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs font-semibold text-slate-400 uppercase">Problems Solved</span>
            <div className="text-2xl font-black text-white mt-0.5">{stats.solved_questions_count || 0} / {stats.total_questions_count || 20}</div>
          </div>
        </div>

        <div className="bg-slate-900/90 p-5 rounded-2xl border border-slate-800 shadow-xl flex items-center gap-4">
          <div className="p-3 rounded-xl bg-cyan-600/20 text-cyan-400 border border-cyan-500/30">
            <Cpu className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs font-semibold text-slate-400 uppercase">Total Submissions</span>
            <div className="text-2xl font-black text-white mt-0.5">{stats.total_submissions || 0}</div>
          </div>
        </div>

        <div className="bg-slate-900/90 p-5 rounded-2xl border border-slate-800 shadow-xl flex items-center gap-4">
          <div className="p-3 rounded-xl bg-violet-600/20 text-violet-400 border border-violet-500/30">
            <Award className="w-6 h-6" />
          </div>
          <div>
            <span className="text-xs font-semibold text-slate-400 uppercase">Success Pass Rate</span>
            <div className="text-2xl font-black text-white mt-0.5">{stats.pass_rate || 0}%</div>
          </div>
        </div>

      </div>

      {/* 3. Recharts Topic Mastery Radar & Bar Chart */}
      <div className="space-y-4">
        <h3 className="text-base font-bold text-white flex items-center gap-2">
          <Award className="w-5 h-5 text-indigo-400" />
          DSA Skill Band & Topic Mastery (Exponential Moving Average)
        </h3>
        <ScoreRadarChart scores={scores} />
      </div>

      {/* 4. Recent Submission History Table */}
      <div className="bg-slate-900/90 p-6 rounded-3xl border border-slate-800 shadow-xl space-y-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-cyan-400" />
            Recent Submission History
          </h3>
          <span className="text-xs text-slate-400 font-mono">
            Showing last {submissions.length} submissions
          </span>
        </div>

        {submissions.length === 0 ? (
          <div className="py-12 text-center text-slate-500 text-xs">
            No submissions recorded yet. Select a question from the bank to start practicing!
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs font-sans">
              <thead className="bg-slate-950 text-slate-400 uppercase font-mono text-[10px]">
                <tr>
                  <th className="py-3 px-4 rounded-l-xl">Status</th>
                  <th className="py-3 px-4">Problem</th>
                  <th className="py-3 px-4">Language</th>
                  <th className="py-3 px-4">Tests Passed</th>
                  <th className="py-3 px-4">Runtime</th>
                  <th className="py-3 px-4">Submitted At</th>
                  <th className="py-3 px-4 rounded-r-xl text-right">AI Feedback</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {submissions.map((sub) => (
                  <tr key={sub.id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-3 px-4">
                      {sub.passed ? (
                        <span className="inline-flex items-center gap-1.5 text-emerald-400 font-bold">
                          <CheckCircle2 className="w-4 h-4" /> Passed
                        </span>
                      ) : (
                        <span className="inline-flex items-center gap-1.5 text-rose-400 font-bold">
                          <XCircle className="w-4 h-4" /> Failed
                        </span>
                      )}
                    </td>

                    <td className="py-3 px-4 font-semibold text-white">
                      <Link to={`/practice/${sub.question_id}`} className="hover:text-indigo-300">
                        {sub.question_title}
                      </Link>
                    </td>

                    <td className="py-3 px-4 font-mono uppercase text-slate-300">
                      {sub.language}
                    </td>

                    <td className="py-3 px-4 font-mono text-slate-300">
                      {sub.passed_count} / {sub.total_tests}
                    </td>

                    <td className="py-3 px-4 font-mono text-cyan-300">
                      {sub.runtime_ms} ms
                    </td>

                    <td className="py-3 px-4 text-slate-400 font-mono">
                      {new Date(sub.created_at).toLocaleDateString()}
                    </td>

                    <td className="py-3 px-4 text-right">
                      {sub.ai_feedback ? (
                        <button
                          onClick={() => setSelectedSubmission(selectedSubmission?.id === sub.id ? null : sub)}
                          className="px-3 py-1 rounded-lg bg-indigo-600/20 hover:bg-indigo-600/40 text-indigo-300 text-[11px] font-semibold border border-indigo-500/30 transition-all"
                        >
                          {selectedSubmission?.id === sub.id ? "Hide Feedback" : "View AI Review"}
                        </button>
                      ) : (
                        <span className="text-slate-600">-</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Selected Submission Inspector Drawer */}
        {selectedSubmission && selectedSubmission.ai_feedback && (
          <div className="mt-6 pt-6 border-t border-slate-800">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-3">
              AI Code Review Inspector — {selectedSubmission.question_title}
            </h4>
            <AIFeedback feedback={selectedSubmission.ai_feedback} />
          </div>
        )}
      </div>

    </div>
  );
};
