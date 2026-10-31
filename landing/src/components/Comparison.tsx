import React from 'react';
import { XCircle, CheckCircle2, AlertTriangle, Check } from 'lucide-react';

export const Comparison: React.FC = () => {
  return (
    <section id="benchmark" className="py-24 border-t border-white/[0.06] relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <span className="font-mono text-xs text-rose-400 uppercase tracking-widest font-semibold">
            THE PROBLEM &bull; UNGROUNDED AI
          </span>
          <h2 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight mt-2">
            Scientific Research Deserves Better Than AI Guesswork.
          </h2>
          <p className="text-slate-400 text-base mt-4">
            In biomedical science and healthcare, unverified claims and fabricated references are unacceptable. See how EvidenceBot differs from conventional chatbots.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 max-w-5xl mx-auto">
          
          {/* LEFT CARD — Conventional AI Chatbots */}
          <div className="p-8 rounded-xl border border-rose-500/20 bg-rose-950/10 backdrop-blur-md relative overflow-hidden">
            <div className="flex items-center space-x-2.5 mb-6 text-rose-400 font-mono text-xs uppercase tracking-wider font-bold">
              <XCircle className="w-4 h-4 text-rose-400" />
              <span>Conventional AI Chatbots</span>
            </div>

            <h3 className="text-xl font-bold text-white mb-6">
              Prone to Hallucinations & Fabricated Citations
            </h3>

            <ul className="space-y-4 text-sm text-slate-300">
              <li className="flex items-start space-x-3">
                <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                <span>Can produce plausible but unsupported scientific statements.</span>
              </li>
              <li className="flex items-start space-x-3">
                <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                <span>May generate incorrect or unverifiable references.</span>
              </li>
              <li className="flex items-start space-x-3">
                <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                <span>Can confuse correlation with causation.</span>
              </li>
              <li className="flex items-start space-x-3">
                <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                <span>May answer confidently even when evidence is limited.</span>
              </li>
              <li className="flex items-start space-x-3">
                <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
                <span>May not provide transparent source retrieval.</span>
              </li>
            </ul>
          </div>

          {/* RIGHT CARD — EvidenceBot */}
          <div className="p-8 rounded-xl border border-sky-500/30 bg-[#090E17]/90 shadow-[0_0_35px_-10px_rgba(14,165,233,0.2)] relative overflow-hidden">
            <div className="flex items-center space-x-2.5 mb-6 text-sky-400 font-mono text-xs uppercase tracking-wider font-bold">
              <CheckCircle2 className="w-4 h-4 text-[#10B981]" />
              <span>EvidenceBot Architecture</span>
            </div>

            <h3 className="text-xl font-bold text-white mb-6">
              Grounded Literature Synthesis & Traceable PMIDs
            </h3>

            <ul className="space-y-4 text-sm text-slate-300">
              <li className="flex items-start space-x-3">
                <Check className="w-4 h-4 text-[#10B981] shrink-0 mt-0.5" />
                <span>Retrieves biomedical literature before generating answers.</span>
              </li>
              <li className="flex items-start space-x-3">
                <Check className="w-4 h-4 text-[#10B981] shrink-0 mt-0.5" />
                <span>Uses semantic similarity to identify relevant passages.</span>
              </li>
              <li className="flex items-start space-x-3">
                <Check className="w-4 h-4 text-[#10B981] shrink-0 mt-0.5" />
                <span>Grounds generated responses in retrieved research excerpts.</span>
              </li>
              <li className="flex items-start space-x-3">
                <Check className="w-4 h-4 text-[#10B981] shrink-0 mt-0.5" />
                <span>Provides PMID links to original PubMed records.</span>
              </li>
              <li className="flex items-start space-x-3">
                <Check className="w-4 h-4 text-[#10B981] shrink-0 mt-0.5" />
                <span>Can communicate when retrieved evidence is insufficient.</span>
              </li>
            </ul>
          </div>

        </div>
      </div>
    </section>
  );
};
export default Comparison;
