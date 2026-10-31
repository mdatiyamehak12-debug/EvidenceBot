import React from 'react';
import { Microscope, TrendingUp, GraduationCap } from 'lucide-react';

export const Personas: React.FC = () => {
  return (
    <section id="capabilities" className="py-24 border-t border-white/[0.06] relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <span className="font-mono text-xs text-sky-400 uppercase tracking-widest font-semibold">
            AUDIENCE PERSONAS
          </span>
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight mt-2">
            Built for People Who Work With Scientific Evidence
          </h2>
          <p className="text-slate-400 text-sm sm:text-base mt-3">
            Designed for critical researchers who cannot afford hallucinations in their workflows.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 max-w-6xl mx-auto">
          {/* Persona 1: Clinical Researchers */}
          <div className="p-7 rounded-xl bg-[#0D1322]/75 border border-white/[0.08] backdrop-blur-md flex flex-col justify-between hover:border-sky-500/40 transition-all hover:-translate-y-1 shadow-sm">
            <div>
              <div className="w-10 h-10 rounded-lg bg-sky-500/10 border border-sky-500/20 flex items-center justify-center text-sky-400 mb-5">
                <Microscope className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">
                Clinical Researchers
              </h3>
              <p className="text-slate-400 text-xs leading-relaxed mb-6">
                Explore biomedical publications, identify relevant findings, and accelerate early-stage literature reviews.
              </p>
            </div>
            <div className="pt-4 border-t border-white/[0.08] text-xs font-medium text-sky-400/90 italic">
              "Spend less time searching across publications and more time evaluating the evidence."
            </div>
          </div>

          {/* Persona 2: Biotech Analysts */}
          <div className="p-7 rounded-xl bg-[#0D1322]/75 border border-white/[0.08] backdrop-blur-md flex flex-col justify-between hover:border-sky-500/40 transition-all hover:-translate-y-1 shadow-sm">
            <div>
              <div className="w-10 h-10 rounded-lg bg-sky-500/10 border border-sky-500/20 flex items-center justify-center text-sky-400 mb-5">
                <TrendingUp className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">
                Biotech Analysts
              </h3>
              <p className="text-slate-400 text-xs leading-relaxed mb-6">
                Explore scientific publications and investigate biological mechanisms relevant to emerging life-sciences technologies.
              </p>
            </div>
            <div className="pt-4 border-t border-white/[0.08] text-xs font-medium text-sky-400/90 italic">
              "Bring scientific literature into the research and due-diligence workflow."
            </div>
          </div>

          {/* Persona 3: Medical and Pharmacology Students */}
          <div className="p-7 rounded-xl bg-[#0D1322]/75 border border-white/[0.08] backdrop-blur-md flex flex-col justify-between hover:border-emerald-500/40 transition-all hover:-translate-y-1 shadow-sm">
            <div>
              <div className="w-10 h-10 rounded-lg bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 mb-5">
                <GraduationCap className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">
                Medical & Pharmacology Students
              </h3>
              <p className="text-slate-400 text-xs leading-relaxed mb-6">
                Explore primary research, understand scientific findings, and follow references back to original publications.
              </p>
            </div>
            <div className="pt-4 border-t border-white/[0.08] text-xs font-medium text-emerald-400/90 italic">
              "Learn from research evidence instead of relying only on generated summaries."
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
export default Personas;

