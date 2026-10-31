import React from 'react';
import { ExternalLink } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer id="about" className="border-t border-white/[0.08] bg-[#06090E] py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row items-start justify-between gap-8 pb-10 border-b border-white/[0.06]">
          
          {/* Brand & Mission Statement */}
          <div className="max-w-sm">
            <div className="flex items-center space-x-2.5 mb-3">
              <div className="w-6 h-6 rounded-md bg-gradient-to-br from-cyan-500/20 to-emerald-500/10 border border-cyan-500/30 flex items-center justify-center p-0.5">
                <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-full h-full">
                  <path d="M12 8C12 8 20 14 20 20C20 26 12 32 12 32" stroke="#0EA5E9" strokeWidth="2.5" strokeLinecap="round" />
                  <path d="M28 8C28 8 20 14 20 20C20 26 28 32 28 32" stroke="#38BDF8" strokeWidth="2.5" strokeLinecap="round" />
                  <circle cx="20" cy="20" r="3" fill="#10B981" />
                </svg>
              </div>
              <span className="text-base font-bold text-white tracking-tight">EvidenceBot</span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Biomedical Literature Intelligence Engine. Grounded scientific discovery powered by NCBI PubMed and dense vector retrieval.
            </p>
          </div>

          {/* Directory Links */}
          <div className="grid grid-cols-2 sm:grid-cols-3 gap-8 text-xs text-slate-400 font-medium">
            <div>
              <div className="font-mono text-[11px] text-white uppercase tracking-wider mb-3">
                Platform
              </div>
              <ul className="space-y-2">
                <li><a href="#capabilities" className="hover:text-sky-400 transition-colors">Capabilities</a></li>
                <li><a href="#architecture" className="hover:text-sky-400 transition-colors">Architecture</a></li>
                <li><a href="#telemetry" className="hover:text-sky-400 transition-colors">Telemetry</a></li>
              </ul>
            </div>
            <div>
              <div className="font-mono text-[11px] text-white uppercase tracking-wider mb-3">
                External
              </div>
              <ul className="space-y-2">
                <li>
                  <a 
                    href="https://github.com/mdatiyamehak12-debug/EvidenceBot" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="hover:text-sky-400 transition-colors inline-flex items-center"
                  >
                    <span>GitHub Repository</span>
                    <ExternalLink className="w-3 h-3 ml-1" />
                  </a>
                </li>
                <li>
                  <a 
                    href="https://pubmed.ncbi.nlm.nih.gov/" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="hover:text-sky-400 transition-colors inline-flex items-center"
                  >
                    <span>PubMed (NLM)</span>
                    <ExternalLink className="w-3 h-3 ml-1" />
                  </a>
                </li>
                <li>
                  <a 
                    href="https://www.ncbi.nlm.nih.gov/home/about/" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="hover:text-sky-400 transition-colors inline-flex items-center"
                  >
                    <span>NCBI Entrez</span>
                    <ExternalLink className="w-3 h-3 ml-1" />
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <div className="font-mono text-[11px] text-white uppercase tracking-wider mb-3">
                Governance
              </div>
              <ul className="space-y-2">
                <li><span className="text-slate-500">Version: v1.0.0</span></li>
                <li><span className="text-slate-500">Status: Stage 1 Prototype</span></li>
                <li><span className="text-slate-500">License: MIT Open Source</span></li>
              </ul>
            </div>
          </div>
        </div>

        {/* Legal Disclaimer & Copyright Notice */}
        <div className="pt-8 flex flex-col md:flex-row items-center justify-between text-[11px] text-slate-500 space-y-4 md:space-y-0">
          <p className="max-w-3xl leading-relaxed">
            <strong>Institutional Notice:</strong> For scientific research and educational discovery only. EvidenceBot is not a medical device and does not provide medical diagnosis or treatment recommendations. Always consult original research publications and qualified healthcare professionals.
          </p>
          <div className="font-mono text-slate-500 shrink-0">
            EVIDENCEBOT &bull; STAGE 1 RESEARCH PROTOTYPE
          </div>
        </div>
      </div>
    </footer>
  );
};
export default Footer;

