import React from 'react';
import { ArrowRight, Layers } from 'lucide-react';

interface CallToActionProps {
  appUrl?: string;
}

export const CallToAction: React.FC<CallToActionProps> = ({ 
  appUrl = 'https://affected-investigate-exam-decorative.trycloudflare.com' 
}) => {
  return (
    <section className="py-20 border-t border-white/[0.06] relative">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="p-10 sm:p-14 rounded-2xl border border-sky-500/30 bg-gradient-to-b from-[#0B1220] to-[#06090E] shadow-[0_0_50px_-10px_rgba(14,165,233,0.25)] text-center relative overflow-hidden">
          
          {/* Ambient Top Glow */}
          <div className="absolute -top-24 left-1/2 -translate-x-1/2 w-96 h-48 bg-sky-500/20 blur-3xl pointer-events-none"></div>

          <span className="font-mono text-xs text-sky-400 uppercase tracking-widest font-semibold">
            GET STARTED TODAY
          </span>
          <h2 className="text-3xl sm:text-5xl font-extrabold text-white tracking-tight mt-3 mb-4">
            Better Biomedical Research Starts With Better Evidence.
          </h2>
          <p className="text-slate-400 text-sm sm:text-base max-w-2xl mx-auto mb-8 leading-relaxed">
            Explore biomedical literature with an AI assistant designed to retrieve sources, ground its responses, and communicate uncertainty.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <a 
              href={appUrl} 
              target="_blank" 
              rel="noopener noreferrer"
              className="w-full sm:w-auto inline-flex items-center justify-center px-8 py-3.5 rounded-md bg-[#0EA5E9] hover:bg-[#38BDF8] text-white font-semibold text-sm tracking-tight shadow-[0_0_35px_-5px_rgba(14,165,233,0.3)] transition-all transform hover:-translate-y-0.5"
            >
              <span>Launch EvidenceBot Free</span>
              <ArrowRight className="w-4 h-4 ml-2" />
            </a>
            <a 
              href="#architecture" 
              className="w-full sm:w-auto inline-flex items-center justify-center px-8 py-3.5 rounded-md bg-white/[0.05] hover:bg-white/[0.1] border border-white/[0.1] text-white font-semibold text-sm tracking-tight transition-all"
            >
              <span>Explore Architecture</span>
              <Layers className="w-4 h-4 ml-2 text-slate-400" />
            </a>
          </div>
        </div>
      </div>
    </section>
  );
};
export default CallToAction;
