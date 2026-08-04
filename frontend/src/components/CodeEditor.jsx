import React from 'react';
import Editor from '@monaco-editor/react';
import { Play, RotateCcw, Code2, Terminal } from 'lucide-react';

export const CodeEditor = ({
  language,
  setLanguage,
  code,
  setCode,
  onSubmit,
  isExecuting,
  onReset
}) => {
  const handleEditorChange = (value) => {
    setCode(value || '');
  };

  return (
    <div className="flex flex-col h-full bg-slate-900/90 rounded-2xl border border-slate-800 overflow-hidden shadow-2xl">
      {/* Editor Control Bar */}
      <div className="flex items-center justify-between px-4 py-3 bg-slate-950/80 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 px-3 py-1 rounded-lg bg-slate-900 border border-slate-800 text-xs font-semibold text-slate-300">
            <Code2 className="w-3.5 h-3.5 text-indigo-400" />
            Language:
          </div>
          
          <div className="flex bg-slate-900 p-1 rounded-xl border border-slate-800">
            <button
              onClick={() => setLanguage('python')}
              className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                language === 'python'
                  ? 'bg-indigo-600 text-white shadow-md'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Python 3
            </button>
            <button
              onClick={() => setLanguage('cpp')}
              className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                language === 'cpp'
                  ? 'bg-indigo-600 text-white shadow-md'
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              C++ (g++)
            </button>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-2">
          {onReset && (
            <button
              onClick={onReset}
              title="Reset Code Snippet"
              className="p-2 rounded-xl text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-colors"
            >
              <RotateCcw className="w-4 h-4" />
            </button>
          )}

          <button
            onClick={onSubmit}
            disabled={isExecuting}
            className="flex items-center gap-2 px-5 py-2 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white text-xs font-bold shadow-lg shadow-emerald-600/20 disabled:opacity-50 transition-all border border-emerald-400/20"
          >
            {isExecuting ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                Executing & Analyzing...
              </>
            ) : (
              <>
                <Play className="w-3.5 h-3.5 fill-white" />
                Submit Solution
              </>
            )}
          </button>
        </div>
      </div>

      {/* Monaco Code Editor Area */}
      <div className="flex-1 min-h-[380px] w-full relative">
        <Editor
          height="100%"
          language={language === 'python' ? 'python' : 'cpp'}
          theme="vs-dark"
          value={code}
          onChange={handleEditorChange}
          options={{
            fontSize: 14,
            fontFamily: "'Fira Code', monospace",
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            automaticLayout: true,
            tabSize: 4,
            lineNumbers: 'on',
            renderLineHighlight: 'all',
            padding: { top: 12, bottom: 12 },
          }}
        />
      </div>

      {/* Bottom Status Indicator */}
      <div className="flex items-center justify-between px-4 py-2 bg-slate-950/60 border-t border-slate-800 text-[11px] text-slate-400 font-mono">
        <div className="flex items-center gap-2">
          <Terminal className="w-3.5 h-3.5 text-cyan-400" />
          <span>Execution Sandbox: Active (5.0s Timeout Limit)</span>
        </div>
        <span>Monaco Editor v0.46</span>
      </div>
    </div>
  );
};
