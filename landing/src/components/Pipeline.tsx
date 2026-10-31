import React from 'react';
import { ArrowRight } from 'lucide-react';

export const Pipeline: React.FC = () => {
  const stages = [
    {
      num: "01",
      phase: "LITERATURE INGESTION",
      title: "Live PubMed Retrieval",
      description: "Connects to the NCBI PubMed E-Utilities API to search biomedical literature and retrieve available abstracts.",
      tech: "NCBI E-UTILITIES / XML",
      color: "text-sky-400",
      badgeColor: "border-sky-500/30 text-sky-400"
    },
    {
      num: "02",
      phase: "SEMANTIC REPRESENTATION",
      title: "Dense Vector Embeddings",
      description: "Sentence Transformers converts research passages and user queries into 384-dimensional numerical representations.",
      tech: "ALL-MINILM-L6-V2 / 384-D",
      color: "text-sky-400",
      badgeColor: "border-sky-500/30 text-sky-400"
    },
    {
      num: "03",
      phase: "EVIDENCE RETRIEVAL",
      title: "FAISS Similarity Search",
      description: "FAISS compares normalized vector embeddings to identify research passages that are semantically relevant to the user's question.",
      tech: "FAISS / COSINE SIMILARITY",
      color: "text-sky-400",
      badgeColor: "border-sky-500/30 text-sky-400"
    },
    {
      num: "04",
      phase: "ANSWER GENERATION",
      title: "Evidence-Grounded Responses",
      description: "An optional OpenAI language model generates a response using retrieved evidence, with references to the corresponding PubMed records.",
      tech: "OPTIONAL LLM / PMID REFERENCES",
      color: "text-[#10B981]",
      badgeColor: "border-emerald-500/30 text-emerald-400"
    }
  ];

  return (
    <section id="architecture" className="py-24 border-t border-white/[0.06] bg-[#090E17]/60">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <span className="font-mono text-xs text-sky-400 uppercase tracking-widest font-semibold">
            EXECUTION ARCHITECTURE
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight mt-2">
            From Research Question to Scientific Evidence
          </h2>
          <p className="text-slate-400 text-sm sm:text-base mt-3">
            An autonomous four-stage pipeline designed for empirical precision and literature provenance.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 relative">
          {stages.map((stage, idx) => (
            <div 
              key={stage.num}
              className="p-6 rounded-xl bg-[#0D1322]/75 border border-white/[0.08] backdrop-blur-md flex flex-col justify-between hover:border-sky-500/40 transition-all hover:-translate-y-1 shadow-sm relative group"
            >
              {/* Desktop Horizontal Flow Indicator */}
              {idx < 3 && (
                <div className="hidden md:block absolute -right-3 top-1/2 -translate-y-1/2 z-10 text-slate-600 group-hover:text-sky-400 transition-colors">
                  <ArrowRight className="w-5 h-5" />
                </div>
              )}

              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className={`font-mono text-xs uppercase tracking-widest font-bold ${stage.color}`}>
                    Stage {stage.num}
                  </span>
                  <span className="font-mono text-[9px] text-slate-500 uppercase tracking-wider">
                    {stage.phase}
                  </span>
                </div>
                <h3 className="text-lg font-bold text-white mt-1 mb-3">
                  {stage.title}
                </h3>
                <p className="text-slate-400 text-xs leading-relaxed">
                  {stage.description}
                </p>
              </div>

              <div className="mt-6 pt-4 border-t border-white/[0.06] font-mono text-[10px] text-slate-500 uppercase tracking-wider flex items-center justify-between">
                <span>{stage.tech}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};
export default Pipeline;
