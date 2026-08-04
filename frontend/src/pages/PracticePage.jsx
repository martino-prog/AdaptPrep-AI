import React, { useState, useEffect } from 'react';
import { useParams, useLocation, useNavigate } from 'react-router-dom';
import { fetchQuestionById, submitCode, fetchNextQuestion } from '../services/api';
import { CodeEditor } from '../components/CodeEditor';
import { TestResults } from '../components/TestResults';
import { AIFeedback } from '../components/AIFeedback';
import { Sparkles, ArrowLeft, Tag, Layers, CheckCircle2, ChevronRight } from 'lucide-react';

export const PracticePage = () => {
  const { id } = useParams();
  const location = useLocation();
  const navigate = useNavigate();

  const [question, setQuestion] = useState(null);
  const [language, setLanguage] = useState('python');
  const [code, setCode] = useState('');
  const [loading, setLoading] = useState(true);
  
  const [isExecuting, setIsExecuting] = useState(false);
  const [executionResponse, setExecutionResponse] = useState(null);
  const [recommendationInfo, setRecommendationInfo] = useState(location.state?.recommendation || null);

  useEffect(() => {
    const loadQuestion = async () => {
      setLoading(true);
      setExecutionResponse(null);
      try {
        const q = await fetchQuestionById(id);
        setQuestion(q);
        // Load starter code
        if (q.starter_code) {
          const starter = q.starter_code[language] || q.starter_code['python'] || '';
          setCode(starter);
        }
      } catch (err) {
        console.error("Failed to fetch question:", err);
      } finally {
        setLoading(false);
      }
    };
    loadQuestion();
  }, [id]);

  // Update code snippet when language toggles
  useEffect(() => {
    if (question && question.starter_code) {
      setCode(question.starter_code[language] || '');
    }
  }, [language, question]);

  const handleResetCode = () => {
    if (question && question.starter_code) {
      setCode(question.starter_code[language] || '');
    }
  };

  const handleSubmitSolution = async () => {
    if (!code.trim()) return;
    setIsExecuting(true);
    setExecutionResponse(null);

    try {
      const res = await submitCode(question.id, language, code);
      setExecutionResponse(res);
    } catch (err) {
      console.error("Submission failed:", err);
    } finally {
      setIsExecuting(false);
    }
  };

  const handleNextAdaptive = async () => {
    try {
      const rec = await fetchNextQuestion();
      if (rec && rec.question) {
        setRecommendationInfo(rec);
        navigate(`/practice/${rec.question.id}`, { state: { recommendation: rec } });
      }
    } catch (err) {
      console.error("Failed to load next question:", err);
    }
  };

  if (loading) {
    return (
      <div className="py-20 flex justify-center items-center">
        <div className="w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    );
  }

  if (!question) {
    return (
      <div className="max-w-4xl mx-auto py-16 text-center space-y-4">
        <h3 className="text-xl font-bold text-white">Question Not Found</h3>
        <button
          onClick={() => navigate('/questions')}
          className="px-4 py-2 rounded-xl bg-indigo-600 text-white text-xs font-semibold"
        >
          Return to Question Bank
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-[1600px] mx-auto px-4 sm:px-6 py-6 space-y-6">
      
      {/* Adaptive Recommendation Hero Banner (if navigated adaptively) */}
      {recommendationInfo && (
        <div className="bg-gradient-to-r from-violet-950/80 via-indigo-950/80 to-slate-900 p-4 rounded-2xl border border-violet-800/60 shadow-lg flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-violet-600/30 text-cyan-300 border border-violet-500/40">
              <Sparkles className="w-5 h-5 text-cyan-300 animate-pulse" />
            </div>
            <div>
              <span className="text-xs font-bold uppercase tracking-wider text-violet-300 block">
                Adaptive Recommendation Triggered
              </span>
              <p className="text-xs text-slate-300">
                {recommendationInfo.reason}
              </p>
            </div>
          </div>
          <button
            onClick={() => setRecommendationInfo(null)}
            className="text-xs text-slate-400 hover:text-white px-2 py-1"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Navigation Top Bar */}
      <div className="flex items-center justify-between">
        <button
          onClick={() => navigate('/questions')}
          className="flex items-center gap-2 text-xs font-semibold text-slate-400 hover:text-slate-200 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          Back to Question Bank
        </button>

        <button
          onClick={handleNextAdaptive}
          className="flex items-center gap-2 px-3.5 py-1.5 rounded-xl bg-violet-600/20 hover:bg-violet-600/40 text-violet-300 text-xs font-bold transition-all border border-violet-500/40"
        >
          <Sparkles className="w-3.5 h-3.5 text-cyan-300" />
          Next Adaptive Recommendation
          <ChevronRight className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Main Split Screen Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Column: Problem Description & Requirements (5 Cols) */}
        <div className="lg:col-span-5 space-y-6">
          <div className="bg-slate-900/90 p-6 rounded-2xl border border-slate-800 shadow-xl space-y-4">
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-md bg-slate-950 text-cyan-300 border border-slate-800">
                {question.topic}
              </span>
              <span className="text-xs font-bold px-2.5 py-0.5 rounded-md bg-indigo-500/10 text-indigo-400 border border-indigo-500/30 capitalize">
                {question.difficulty}
              </span>
            </div>

            <h1 className="text-2xl font-extrabold text-white tracking-tight">
              {question.title}
            </h1>

            <div className="text-xs text-slate-300 leading-relaxed whitespace-pre-wrap font-sans space-y-2 border-t border-b border-slate-800/80 py-4">
              {question.description}
            </div>

            {/* Sample Test Cases Preview */}
            <div className="space-y-3 pt-2">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400">
                Sample Test Cases
              </h4>
              {question.test_cases && question.test_cases.slice(0, 2).map((tc, idx) => (
                <div key={idx} className="p-3 rounded-xl bg-slate-950 border border-slate-800 font-mono text-xs space-y-1">
                  <div className="text-slate-400">Sample Input {idx + 1}: <span className="text-slate-200 font-semibold">{tc.input}</span></div>
                  <div className="text-slate-400">Expected Output: <span className="text-emerald-400 font-semibold">{tc.expected}</span></div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: Code Editor & Execution Panel (7 Cols) */}
        <div className="lg:col-span-7 space-y-6 flex flex-col">
          
          {/* Monaco Code Editor */}
          <CodeEditor
            language={language}
            setLanguage={setLanguage}
            code={code}
            setCode={setCode}
            onSubmit={handleSubmitSolution}
            isExecuting={isExecuting}
            onReset={handleResetCode}
          />

          {/* Test Case Execution Output Panel */}
          {executionResponse && executionResponse.execution && (
            <TestResults
              execution={executionResponse.execution}
              topicScoreUpdate={executionResponse.updated_topic_score}
            />
          )}

          {/* LangChain AI Review Panel */}
          {executionResponse && executionResponse.ai_feedback && (
            <AIFeedback feedback={executionResponse.ai_feedback} />
          )}

        </div>

      </div>

    </div>
  );
};
