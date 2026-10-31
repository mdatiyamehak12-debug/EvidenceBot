import React from 'react';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Telemetry from './components/Telemetry';
import Comparison from './components/Comparison';
import Pipeline from './components/Pipeline';
import Personas from './components/Personas';
import CallToAction from './components/CallToAction';
import Footer from './components/Footer';

export const App: React.FC = () => {
  const liveAppUrl = 'https://affected-investigate-exam-decorative.trycloudflare.com';

  return (
    <div className="min-h-screen bg-[#06090E] text-[#F8FAFC] font-sans antialiased selection:bg-[#0EA5E9] selection:text-white relative overflow-x-hidden">
      {/* Background Ambient Radial Glows */}
      <div className="fixed top-0 left-1/2 -translate-x-1/2 w-[900px] h-[450px] bg-sky-500/10 blur-[130px] rounded-full pointer-events-none -z-10" />
      <div className="fixed bottom-0 right-0 w-[600px] h-[350px] bg-emerald-500/5 blur-[140px] rounded-full pointer-events-none -z-10" />

      {/* SECTION 1: Fixed Navigation Bar */}
      <Navbar appUrl={liveAppUrl} />

      {/* Main Content Sections */}
      <main>
        {/* SECTION 2: Hero Section + Interactive Search Simulator */}
        <Hero appUrl={liveAppUrl} />

        {/* SECTION 3: Platform Telemetry */}
        <Telemetry />

        {/* SECTION 4: The Problem vs The Solution Matrix */}
        <Comparison />

        {/* SECTION 5: Four-Stage Autonomous Pipeline */}
        <Pipeline />

        {/* SECTION 6: Target Personas */}
        <Personas />

        {/* SECTION 7: Final Call To Action */}
        <CallToAction appUrl={liveAppUrl} />
      </main>

      {/* SECTION 8: Institutional Footer */}
      <Footer />
    </div>
  );
};

export default App;
