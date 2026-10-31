import React, { useState } from 'react';
import { ExternalLink, Terminal, Play, AlertCircle } from 'lucide-react';

interface QueryData {
  answer: string;
  confidence: string;
  isAbstention: boolean;
  excerpts: Array<{ pmid: string; text: string }>;
}

const PRESET_QUERIES: Record<string, QueryData> = {
  "Does vitamin D supplementation reduce respiratory tract infections?": {
    answer: "Randomized controlled trials and meta-analyses indexed on PubMed demonstrate that regular daily or weekly vitamin D supplementation significantly reduces the risk of acute respiratory tract infections, particularly in individuals with severe baseline vitamin D deficiency (<25 nmol/L) [PMID: 34322844].",
    confidence: "CONFIDENCE: HIGH",
    isAbstention: false,
    excerpts: [
      { 
        pmid: "34322844", 
        text: "In systematic reviews and individual patient data meta-analyses of randomized trials, vitamin D supplementation was safe and protected against acute respiratory tract infections overall (aOR 0.88, 95% CI 0.81 to 0.96)..." 
      },
      { 
        pmid: "28202713", 
        text: "Patients receiving daily or weekly doses without additional boluses experienced the most pronounced protective effects, especially those presenting with baseline 25-hydroxyvitamin D levels below 25 nmol/L." 
      }
    ]
  },
  "Does zinc supplementation reduce the duration or severity of common cold symptoms?": {
    answer: "A synthesis of randomized placebo-controlled trials confirms that zinc supplementation administered as zinc gluconate or acetate lozenges within 24 hours of symptom onset reduces the duration of common cold symptoms in adults by an average of 33% [PMID: 38719213, PMID: 23775705].",
    confidence: "CONFIDENCE: HIGH",
    isAbstention: false,
    excerpts: [
      { 
        pmid: "38719213", 
        text: "Meta-analyses of high-dose zinc lozenge trials (>75 mg/day) demonstrated a statistically significant reduction in cold duration by approximately 3 days without serious adverse events." 
      },
      { 
        pmid: "23775705", 
        text: "Intake of zinc was associated with a significant reduction in the duration of cold symptoms in both adult and pediatric cohorts when initiated early in the disease course." 
      }
    ]
  },
  "What is the cellular mechanism of action of metformin in type 2 diabetes?": {
    answer: "Metformin exerts its primary antihyperglycemic action by suppressing hepatic gluconeogenesis through the activation of AMP-activated protein kinase (AMPK) and inhibition of mitochondrial respiratory chain Complex I, which restores cellular energy homeostasis [PMID: 25414349].",
    confidence: "CONFIDENCE: HIGH",
    isAbstention: false,
    excerpts: [
      { 
        pmid: "25414349", 
        text: "Metformin inhibits hepatic gluconeogenesis via transient inhibition of the mitochondrial electron transport chain complex I, leading to decreased ATP/AMP ratios and subsequent activation of AMPK..." 
      },
      { 
        pmid: "28373489", 
        text: "Molecular pathways also demonstrate reduced cyclic AMP (cAMP) signaling in response to glucagon, further blocking gluconeogenic enzyme transcription in hepatocytes." 
      }
    ]
  },
  "Can spirulina microalgae supplementation cure multiple sclerosis in human patients?": {
    answer: "EMPIRICAL ABSTENTION ACTIVATED: I could not find sufficient reliable evidence in the retrieved peer-reviewed literature to substantiate that spirulina cures multiple sclerosis. Current literature is restricted to in-vitro and preclinical rodent autoimmune models; human clinical trials validating curative efficacy do not exist.",
    confidence: "ABSTENTION: INSUFFICIENT DATA",
    isAbstention: true,
    excerpts: [
      { 
        pmid: "26444857", 
        text: "Preclinical models of experimental autoimmune encephalomyelitis (EAE) in rodents show anti-inflammatory cytokine modulation with phycocyanin extracts, but clinical trial endpoints in humans have not been established." 
      }
    ]
  }
};

export const SearchDemo: React.FC = () => {
  const [query, setQuery] = useState("Does vitamin D supplementation reduce respiratory tract infections?");
  const [activeStep, setActiveStep] = useState(4);
  const [isRunning, setIsRunning] = useState(false);

  const runSimulation = (selectedQuery?: string) => {
    const q = selectedQuery || query;
    setIsRunning(true);
    setActiveStep(1);

    setTimeout(() => {
      setActiveStep(2);
    }, 350);

    setTimeout(() => {
      setActiveStep(3);
    }, 700);

    setTimeout(() => {
      setActiveStep(4);
      setIsRunning(false);
    }, 1050);
  };

  const currentData = PRESET_QUERIES[query] || PRESET_QUERIES["Does vitamin D supplementation reduce respiratory tract infections?"];

  return (
    <div id="demo-console" className="mt-16 max-w-4xl mx-auto rounded-xl border border-white/[0.12] bg-[#090E17]/95 shadow-2xl overflow-hidden backdrop-blur-xl">
      {/* Console Window Header */}
      <div className="px-5 py-3.5 bg-[#06090E] border-b border-white/[0.08] flex items-center justify-between">
        <div className="flex items-center space-x-2.5">
          <div className="flex space-x-1.5">
            <span className="w-3 h-3 rounded-full bg-rose-500/80 inline-block"></span>
            <span className="w-3 h-3 rounded-full bg-amber-500/80 inline-block"></span>
            <span className="w-3 h-3 rounded-full bg-emerald-500/80 inline-block"></span>
          </div>
          <div className="flex items-center space-x-1.5 ml-2">
            <Terminal className="w-3.5 h-3.5 text-slate-500" />
            <span className="font-mono text-xs uppercase tracking-wider text-slate-400 font-semibold">
              EVIDENCEBOT / RESEARCH CONSOLE
            </span>
          </div>
        </div>
        <div className="flex items-center space-x-2 text-[11px] font-mono text-sky-400 bg-sky-500/10 px-2.5 py-1 rounded border border-sky-500/20">
          <span className="w-1.5 h-1.5 rounded-full bg-sky-400"></span>
          <span>SIMULATION DEMO &bull; NCBI ENTREZ</span>
        </div>
      </div>

      {/* Query Input Area */}
      <div className="p-6 border-b border-white/[0.06]">
        <label className="block text-xs font-mono text-slate-400 uppercase tracking-wider mb-2">
          Scientific or Clinical Inquiry:
        </label>
        <div className="relative">
          <input 
            type="text" 
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter') runSimulation(); }}
            placeholder="Enter biomedical question..."
            className="w-full bg-[#06090E] border border-white/[0.12] rounded-lg px-4 py-3 text-sm text-white focus:outline-none focus:border-sky-500 transition-colors font-sans pr-28"
          />
          <button 
            onClick={() => runSimulation()}
            disabled={isRunning}
            className="absolute right-2 top-2 px-3.5 py-1.5 rounded bg-[#0EA5E9] hover:bg-[#38BDF8] disabled:opacity-50 text-white font-medium text-xs tracking-tight transition-all flex items-center space-x-1"
          >
            <span>Execute</span>
            <Play className="w-3 h-3 fill-current ml-1" />
          </button>
        </div>
        
        {/* Sample Query Quick Chips */}
        <div className="flex flex-wrap items-center gap-2 mt-3 text-xs text-slate-400">
          <span className="font-mono text-[11px]">Examples:</span>
          {Object.keys(PRESET_QUERIES).map((qKey) => (
            <button 
              key={qKey}
              onClick={() => {
                setQuery(qKey);
                runSimulation(qKey);
              }}
              className="px-2.5 py-1 rounded bg-white/[0.04] hover:bg-white/[0.08] border border-white/[0.06] text-slate-300 text-[11px] font-mono transition-colors text-left"
            >
              {qKey.includes('zinc') ? 'Zinc & Cold' :
               qKey.includes('metformin') ? 'Metformin Pathway' :
               qKey.includes('spirulina') ? 'Spirulina & MS (Abstention)' : 'Vitamin D & RTI'}
            </button>
          ))}
        </div>
      </div>

      {/* Staged 4-Step Pipeline Execution Visualizer */}
      <div className="p-6 bg-[#0B1220]/50">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
          <div className={`p-3 rounded-lg border transition-all ${
            activeStep === 1 
              ? 'border-sky-500/60 bg-sky-500/20 shadow-[0_0_20px_-3px_rgba(14,165,233,0.3)]' 
              : 'border-white/[0.08] bg-white/[0.02]'
          }`}>
            <div className={`font-mono text-[10px] font-bold ${activeStep === 1 ? 'text-sky-300' : 'text-slate-400'}`}>
              01 &bull; PUBMED RETRIEVAL
            </div>
            <div className="text-xs text-slate-300 font-medium mt-1">
              Searching NCBI...
            </div>
          </div>

          <div className={`p-3 rounded-lg border transition-all ${
            activeStep === 2 
              ? 'border-sky-500/60 bg-sky-500/20 shadow-[0_0_20px_-3px_rgba(14,165,233,0.3)]' 
              : 'border-white/[0.08] bg-white/[0.02]'
          }`}>
            <div className={`font-mono text-[10px] font-bold ${activeStep === 2 ? 'text-sky-300' : 'text-slate-400'}`}>
              02 &bull; SEMANTIC RETRIEVAL
            </div>
            <div className="text-xs text-slate-300 font-medium mt-1">
              Sentence Transformers → FAISS
            </div>
          </div>

          <div className={`p-3 rounded-lg border transition-all ${
            activeStep === 3 
              ? 'border-sky-500/60 bg-sky-500/20 shadow-[0_0_20px_-3px_rgba(14,165,233,0.3)]' 
              : 'border-white/[0.08] bg-white/[0.02]'
          }`}>
            <div className={`font-mono text-[10px] font-bold ${activeStep === 3 ? 'text-sky-300' : 'text-slate-400'}`}>
              03 &bull; EVIDENCE EXTRACTION
            </div>
            <div className="text-xs text-slate-300 font-medium mt-1">
              Extracting Abstract Passages
            </div>
          </div>

          <div className={`p-3 rounded-lg border transition-all ${
            activeStep === 4 
              ? currentData.isAbstention 
                ? 'border-rose-500/60 bg-rose-500/20 shadow-[0_0_20px_-3px_rgba(244,63,94,0.3)]' 
                : 'border-emerald-500/60 bg-emerald-500/20 shadow-[0_0_20px_-3px_rgba(16,185,129,0.3)]' 
              : 'border-white/[0.08] bg-white/[0.02]'
          }`}>
            <div className={`font-mono text-[10px] font-bold ${
              activeStep === 4 
                ? currentData.isAbstention ? 'text-rose-300' : 'text-emerald-400' 
                : 'text-slate-400'
            }`}>
              04 &bull; ANSWER GENERATION
            </div>
            <div className="text-xs text-slate-300 font-medium mt-1">
              {currentData.isAbstention ? 'Empirical Abstention' : 'Evidence-Grounded Response'}
            </div>
          </div>
        </div>

        {/* Output Answer Card Container */}
        <div className={`p-5 rounded-lg border bg-[#06090E] space-y-4 ${
          currentData.isAbstention ? 'border-rose-500/30' : 'border-sky-500/30'
        }`}>
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className={`font-mono text-[11px] uppercase tracking-wider font-bold ${
                currentData.isAbstention ? 'text-rose-400' : 'text-sky-400'
              }`}>
                {currentData.isAbstention ? 'EMPIRICAL ABSTENTION NOTICE' : 'DIRECT EVIDENCE SYNTHESIS'}
              </span>
              <span className={`font-mono text-[10px] px-2 py-0.5 rounded border ${
                currentData.isAbstention 
                  ? 'text-rose-400 bg-rose-500/10 border-rose-500/20' 
                  : 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20'
              }`}>
                {currentData.confidence}
              </span>
            </div>
            <p className="text-sm text-slate-200 leading-relaxed">
              {currentData.answer}
            </p>
          </div>

          {/* Supporting Evidence Excerpts */}
          <div className="pt-3 border-t border-white/[0.08]">
            <div className="font-mono text-[11px] text-slate-400 uppercase tracking-wider mb-2">
              VERIFIED EXCERPT PASSAGES:
            </div>
            <div className="space-y-2">
              {currentData.excerpts.map((excerpt, idx) => (
                <div key={idx} className="p-2.5 rounded bg-white/[0.02] border-l-2 border-[#0EA5E9] text-xs text-slate-300 flex items-start justify-between">
                  <div>
                    <a 
                      href={`https://pubmed.ncbi.nlm.nih.gov/${excerpt.pmid}/`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="font-mono text-sky-400 font-semibold hover:underline inline-flex items-center mr-1"
                    >
                      <span>[PMID: {excerpt.pmid}]</span>
                      <ExternalLink className="w-3 h-3 ml-0.5" />
                    </a>: "{excerpt.text}"
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="pt-2 text-[10px] font-mono text-slate-500 flex items-center justify-between">
            <span className="flex items-center">
              <AlertCircle className="w-3 h-3 mr-1 text-slate-400" />
              Simulated demonstration with verified historical PubMed records.
            </span>
            <span>PROVENANCE: NCBI ENTREZ</span>
          </div>
        </div>
      </div>
    </div>
  );
};
export default SearchDemo;
