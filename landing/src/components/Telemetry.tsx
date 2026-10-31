import React from 'react';
import { Database, Cpu, Zap, CheckCircle2 } from 'lucide-react';

export const Telemetry: React.FC = () => {
  return (
    <section id="telemetry" className="py-20 border-t border-white/[0.06] bg-[#090E17]/60">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-14">
          <span className="font-mono text-xs text-sky-400 uppercase tracking-widest font-semibold">
            CORE PLATFORM ARCHITECTURE
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight mt-2">
            Platform Telemetry
          </h2>
          <p className="text-slate-400 text-sm sm:text-base mt-3">
            Empirical benchmarks grounded in verified biomedical infrastructure components.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
          {/* Metric 1: PubMed */}
          <div className="p-6 rounded-xl bg-[#0D1322]/75 border border-white/[0.08] backdrop-blur-md hover:border-sky-500/40 transition-all hover:-translate-y-1 shadow-sm hover:shadow-[0_12px_30px_-8px_rgba(14,165,233,0.15)]">
            <div className="flex items-center justify-between mb-4">
              <span className="font-mono text-[11px] text-sky-400 uppercase tracking-wider font-semibold">
                Biomedical literature source
              </span>
              <Database className="w-4 h-4 text-sky-400" />
            </div>
            <div className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
              PubMed
            </div>
            <p className="text-slate-400 text-xs mt-3 leading-relaxed">
              Research retrieval through NCBI E-Utilities API suite.
            </p>
          </div>

          {/* Metric 2: 384-Dim */}
          <div className="p-6 rounded-xl bg-[#0D1322]/75 border border-white/[0.08] backdrop-blur-md hover:border-sky-500/40 transition-all hover:-translate-y-1 shadow-sm hover:shadow-[0_12px_30px_-8px_rgba(14,165,233,0.15)]">
            <div className="flex items-center justify-between mb-4">
              <span className="font-mono text-[11px] text-sky-400 uppercase tracking-wider font-semibold">
                Semantic embeddings
              </span>
              <Cpu className="w-4 h-4 text-sky-400" />
            </div>
            <div className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
              384-Dim
            </div>
            <p className="text-slate-400 text-xs mt-3 leading-relaxed">
              <code className="text-sky-400 font-mono">all-MiniLM-L6-v2</code> sentence embeddings mapping scientific context.
            </p>
          </div>

          {/* Metric 3: FAISS */}
          <div className="p-6 rounded-xl bg-[#0D1322]/75 border border-white/[0.08] backdrop-blur-md hover:border-sky-500/40 transition-all hover:-translate-y-1 shadow-sm hover:shadow-[0_12px_30px_-8px_rgba(14,165,233,0.15)]">
            <div className="flex items-center justify-between mb-4">
              <span className="font-mono text-[11px] text-sky-400 uppercase tracking-wider font-semibold">
                Vector similarity search
              </span>
              <Zap className="w-4 h-4 text-sky-400" />
            </div>
            <div className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
              FAISS
            </div>
            <p className="text-slate-400 text-xs mt-3 leading-relaxed">
              Efficient retrieval of semantically relevant passages via inner-product indexing.
            </p>
          </div>

          {/* Metric 4: PMID */}
          <div className="p-6 rounded-xl bg-[#0D1322]/75 border border-white/[0.08] backdrop-blur-md hover:border-emerald-500/40 transition-all hover:-translate-y-1 shadow-sm hover:shadow-[0_12px_30px_-8px_rgba(16,185,129,0.15)]">
            <div className="flex items-center justify-between mb-4">
              <span className="font-mono text-[11px] text-emerald-400 uppercase tracking-wider font-semibold">
                Source traceability
              </span>
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            </div>
            <div className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight">
              PMID
            </div>
            <p className="text-slate-400 text-xs mt-3 leading-relaxed">
              Direct links to original PubMed records ensuring verifiable evidence provenance.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};
export default Telemetry;

