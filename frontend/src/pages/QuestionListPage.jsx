import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { fetchQuestions } from '../services/api';
import { Code2, Filter, ChevronRight, Layers, Tag, Sparkles } from 'lucide-react';

const TOPICS = [
  { id: '', label: 'All Topics' },
  { id: 'arrays', label: 'Arrays' },
  { id: 'strings', label: 'Strings' },
  { id: 'dp', label: 'Dynamic Programming' },
  { id: 'graphs', label: 'Graphs' },
  { id: 'trees', label: 'Trees & Linked Lists' }
];

const DIFFICULTIES = ['All', 'Easy', 'Medium', 'Hard'];

export const QuestionListPage = () => {
  const [questions, setQuestions] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState('');
  const [selectedDifficulty, setSelectedDifficulty] = useState('All');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadQuestions = async () => {
      setLoading(true);
      try {
        const diff = selectedDifficulty === 'All' ? '' : selectedDifficulty;
        const data = await fetchQuestions(selectedTopic, diff);
        setQuestions(data);
      } catch (err) {
        console.error("Failed to load questions:", err);
      } finally {
        setLoading(false);
      }
    };
    loadQuestions();
  }, [selectedTopic, selectedDifficulty]);

  const getDifficultyBadge = (diff) => {
    switch (diff.toLowerCase()) {
      case 'easy':
        return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30';
      case 'medium':
        return 'bg-amber-500/10 text-amber-400 border-amber-500/30';
      case 'hard':
        return 'bg-rose-500/10 text-rose-400 border-rose-500/30';
      default:
        return 'bg-slate-800 text-slate-300 border-slate-700';
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
      
      {/* Header Banner */}
      <div className="bg-slate-900/90 p-6 rounded-3xl border border-slate-800 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-4 relative overflow-hidden">
        <div className="absolute -right-10 -bottom-10 w-64 h-64 bg-indigo-600/10 rounded-full blur-3xl pointer-events-none"></div>
        <div>
          <h2 className="text-2xl font-black text-white flex items-center gap-3">
            <Code2 className="w-7 h-7 text-indigo-400" />
            DSA Question Bank
          </h2>
          <p className="text-xs text-slate-400 mt-1 max-w-xl">
            Curated placement problem set supporting sandboxed execution in Python 3 & C++ with AI code analysis
          </p>
        </div>

        <div className="flex items-center gap-2 font-mono text-xs text-slate-400 bg-slate-950 px-4 py-2 rounded-2xl border border-slate-800">
          <Layers className="w-4 h-4 text-cyan-400" />
          <span>Total Questions: <strong>{questions.length}</strong></span>
        </div>
      </div>

      {/* Filter Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-4 bg-slate-900/60 p-4 rounded-2xl border border-slate-800">
        {/* Topic Filter Pills */}
        <div className="flex flex-wrap items-center gap-1.5">
          <span className="text-xs font-semibold text-slate-400 mr-2 flex items-center gap-1">
            <Filter className="w-3.5 h-3.5" /> Topic:
          </span>
          {TOPICS.map((t) => (
            <button
              key={t.id}
              onClick={() => setSelectedTopic(t.id)}
              className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                selectedTopic === t.id
                  ? 'bg-indigo-600 text-white shadow-md'
                  : 'bg-slate-950 text-slate-400 hover:text-slate-200 border border-slate-800'
              }`}
            >
              {t.label}
            </button>
          ))}
        </div>

        {/* Difficulty Filter */}
        <div className="flex items-center gap-1.5">
          <span className="text-xs font-semibold text-slate-400 mr-2">Difficulty:</span>
          {DIFFICULTIES.map((diff) => (
            <button
              key={diff}
              onClick={() => setSelectedDifficulty(diff)}
              className={`px-3 py-1.5 rounded-xl text-xs font-semibold transition-all ${
                selectedDifficulty === diff
                  ? 'bg-violet-600 text-white shadow-md'
                  : 'bg-slate-950 text-slate-400 hover:text-slate-200 border border-slate-800'
              }`}
            >
              {diff}
            </button>
          ))}
        </div>
      </div>

      {/* Questions Grid */}
      {loading ? (
        <div className="py-20 flex justify-center items-center">
          <div className="w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
        </div>
      ) : questions.length === 0 ? (
        <div className="bg-slate-900/60 p-12 rounded-3xl border border-slate-800 text-center space-y-3">
          <p className="text-slate-400 text-sm">No questions found matching the selected filters.</p>
          <button
            onClick={() => { setSelectedTopic(''); setSelectedDifficulty('All'); }}
            className="px-4 py-2 rounded-xl bg-indigo-600 text-white text-xs font-semibold"
          >
            Clear Filters
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {questions.map((q) => (
            <div
              key={q.id}
              className="bg-slate-900/90 p-5 rounded-2xl border border-slate-800/80 hover:border-indigo-500/50 shadow-xl transition-all hover:shadow-indigo-500/10 flex flex-col justify-between group"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-[11px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-md bg-slate-950 text-cyan-300 border border-slate-800 flex items-center gap-1">
                    <Tag className="w-3 h-3 text-cyan-400" />
                    {q.topic}
                  </span>
                  <span className={`text-[11px] font-bold px-2.5 py-0.5 rounded-md border capitalize ${getDifficultyBadge(q.difficulty)}`}>
                    {q.difficulty}
                  </span>
                </div>

                <h3 className="text-base font-bold text-white group-hover:text-indigo-300 transition-colors line-clamp-1">
                  {q.title}
                </h3>
                <p className="text-xs text-slate-400 mt-2 line-clamp-2 leading-relaxed">
                  {q.description.replace(/\\n/g, ' ')}
                </p>
              </div>

              <div className="mt-5 pt-4 border-t border-slate-800/60 flex items-center justify-between">
                <span className="text-[11px] text-slate-500 font-mono">ID: #{q.id}</span>
                <Link
                  to={`/practice/${q.id}`}
                  className="flex items-center gap-1.5 px-4 py-1.5 rounded-xl bg-slate-950 hover:bg-indigo-600 text-indigo-300 hover:text-white text-xs font-bold transition-all border border-indigo-500/30"
                >
                  Solve Problem
                  <ChevronRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}

    </div>
  );
};
