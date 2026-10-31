import React, { useState } from 'react';
import { ArrowRight, Menu, X } from 'lucide-react';

interface NavbarProps {
  appUrl?: string;
}

export const Navbar: React.FC<NavbarProps> = ({ 
  appUrl = 'https://affected-investigate-exam-decorative.trycloudflare.com' 
}) => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="fixed top-0 inset-x-0 z-50 bg-[#06090E]/80 backdrop-blur-md border-b border-white/[0.06] transition-all">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand & Status */}
        <a href="#" className="flex items-center space-x-3 group">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-500/20 to-emerald-500/10 border border-cyan-500/30 flex items-center justify-center p-1 group-hover:scale-105 transition-transform">
            <svg viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" className="w-full h-full">
              <path d="M12 8C12 8 20 14 20 20C20 26 12 32 12 32" stroke="#0EA5E9" strokeWidth="2.5" strokeLinecap="round" />
              <path d="M28 8C28 8 20 14 20 20C20 26 28 32 28 32" stroke="#38BDF8" strokeWidth="2.5" strokeLinecap="round" />
              <line x1="16" y1="14" x2="24" y2="14" stroke="#10B981" strokeWidth="2" strokeLinecap="round" />
              <line x1="14" y1="20" x2="26" y2="20" stroke="#10B981" strokeWidth="2" strokeLinecap="round" />
              <line x1="16" y1="26" x2="24" y2="26" stroke="#10B981" strokeWidth="2" strokeLinecap="round" />
              <circle cx="20" cy="20" r="3" fill="#10B981" />
            </svg>
          </div>
          <div className="flex flex-col">
            <span className="text-base font-extrabold tracking-tight text-white group-hover:text-[#38BDF8] transition-colors">
              EvidenceBot
            </span>
            <div className="flex items-center space-x-1.5 -mt-0.5">
              <span className="w-1.5 h-1.5 rounded-full bg-[#10B981] animate-pulse"></span>
              <span className="font-mono text-[9px] uppercase tracking-wider text-emerald-400 font-semibold">
                NCBI PUBMED CONNECTED
              </span>
            </div>
          </div>
        </a>

        {/* Center Desktop Navigation Links */}
        <nav className="hidden md:flex items-center space-x-8 text-sm font-medium text-slate-400">
          <a href="#capabilities" className="hover:text-white transition-colors">Capabilities</a>
          <a href="#architecture" className="hover:text-white transition-colors">Architecture</a>
          <a href="#telemetry" className="hover:text-white transition-colors">Telemetry</a>
          <a href="#benchmark" className="hover:text-white transition-colors">Benchmark</a>
          <a href="#about" className="hover:text-white transition-colors">About</a>
        </nav>

        {/* Right Action & Mobile Toggle */}
        <div className="flex items-center space-x-4">
          <a 
            href={appUrl} 
            target="_blank" 
            rel="noopener noreferrer"
            className="hidden sm:inline-flex items-center px-4 py-2 rounded-md bg-gradient-to-r from-[#0EA5E9] to-[#0284C7] hover:from-[#38BDF8] hover:to-[#0EA5E9] text-white text-xs font-semibold tracking-tight shadow-[0_0_25px_-5px_rgba(14,165,233,0.3)] transition-all transform hover:-translate-y-0.5"
          >
            <span>Launch Platform</span>
            <ArrowRight className="w-3.5 h-3.5 ml-1.5" />
          </a>
          
          <button 
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)} 
            className="md:hidden p-2 text-slate-400 hover:text-white focus:outline-none"
            aria-label="Toggle Navigation Menu"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-[#090E17] border-b border-white/[0.08] px-4 pt-2 pb-4 space-y-2">
          <a 
            href="#capabilities" 
            onClick={() => setMobileMenuOpen(false)}
            className="block px-3 py-2 rounded-md text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5"
          >
            Capabilities
          </a>
          <a 
            href="#architecture" 
            onClick={() => setMobileMenuOpen(false)}
            className="block px-3 py-2 rounded-md text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5"
          >
            Architecture
          </a>
          <a 
            href="#telemetry" 
            onClick={() => setMobileMenuOpen(false)}
            className="block px-3 py-2 rounded-md text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5"
          >
            Telemetry
          </a>
          <a 
            href="#benchmark" 
            onClick={() => setMobileMenuOpen(false)}
            className="block px-3 py-2 rounded-md text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5"
          >
            Benchmark
          </a>
          <a 
            href="#about" 
            onClick={() => setMobileMenuOpen(false)}
            className="block px-3 py-2 rounded-md text-sm font-medium text-slate-400 hover:text-white hover:bg-white/5"
          >
            About
          </a>
          <a 
            href={appUrl} 
            target="_blank" 
            rel="noopener noreferrer"
            className="block w-full text-center px-4 py-2.5 rounded-md bg-[#0EA5E9] text-white text-xs font-bold uppercase tracking-wider mt-2"
          >
            Launch Platform &rarr;
          </a>
        </div>
      )}
    </header>
  );
};
export default Navbar;
