import React from 'react';
import { ArrowRight, Layers, Database, Cpu, ShieldCheck } from 'lucide-react';
import SearchDemo from './SearchDemo';

interface HeroProps {
  appUrl?: string;
}

export const Hero: React.FC<HeroProps> = ({ 
  appUrl = 'https://affected-investigate-exam-decorative.trycloudflare.com' 
}) => {
  return (
    <section className="pt-32 pb-20 md:pt-40 md:pb-28 relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Center Hero Content */}
        <div className="text-center max-w-4xl mx-auto">
          {/* Status Badge */}
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-sky-500/10 border border-sky-500/30 text-sky-400 mb-6">
            <span className="w-1.5 h-1.5 rounded-full bg-[#0EA5E9]"></span>
            <span className="font-mono text-xs uppercase tracking-widest font-semibold">
              Biomedical Literature Intelligence Engine
            </span>
          </div>

          {/* Main Headline */}
          <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-white leading-[1.08] mb-6">
            Autonomous Biomedical Intelligence.<br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#38BDF8] via-white to-[#10B981]">
              Grounded in Evidence. Built to Abstain.
            </span>
          </h1>

          {/* Subheadline */}
          <p className="text-base sm:text-xl text-slate-400 font-normal max-w-3xl mx-auto mb-10 leading-relaxed">
            Search biomedical research, retrieve relevant scientific evidence, and generate research answers with traceable PubMed references. EvidenceBot puts scientific literature at the center of every response.
          </p>

          {/* Action CTAs */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-14">
            <a 
              href={appUrl} 
              target="_blank" 
              rel="noopener noreferrer"
              className="w-full sm:w-auto inline-flex items-center justify-center px-7 py-3.5 rounded-md bg-[#0EA5E9] hover:bg-[#38BDF8] text-white font-semibold text-sm tracking-tight shadow-[0_0_35px_-5px_rgba(14,165,233,0.3)] transition-all transform hover:-translate-y-0.5"
            >
              <span>Launch EvidenceBot Free</span>
              <ArrowRight className="w-4 h-4 ml-2" />
            </a>
            <a 
              href="#architecture" 
              className="w-full sm:w-auto inline-flex items-center justify-center px-7 py-3.5 rounded-md bg-white/[0.05] hover:bg-white/[0.1] border border-white/[0.1] text-white font-semibold text-sm tracking-tight transition-all"
            >
              <span>Explore Architecture</span>
              <Layers className="w-4 h-4 ml-2 text-slate-400" />
            </a>
          </div>

          {/* 3 Technical Indicators */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 max-w-3xl mx-auto pt-4 border-t border-white/[0.06]">
            <div className="flex items-center justify-center space-x-2 text-xs font-mono text-slate-400 uppercase tracking-wider">
              <Database className="w-3.5 h-3.5 text-sky-400" />
              <span>PubMed Literature Retrieval</span>
            </div>
            <div className="flex items-center justify-center space-x-2 text-xs font-mono text-slate-400 uppercase tracking-wider">
              <Cpu className="w-3.5 h-3.5 text-[#0EA5E9]" />
              <span>Semantic Vector Search</span>
            </div>
            <div className="flex items-center justify-center space-x-2 text-xs font-mono text-slate-400 uppercase tracking-wider">
              <ShieldCheck className="w-3.5 h-3.5 text-[#10B981]" />
              <span>Evidence-Grounded Answers</span>
            </div>
          </div>
        </div>

        {/* Interactive Search Console Simulation */}
        <SearchDemo />

      </div>
    </section>
  );
};
export default Hero;
