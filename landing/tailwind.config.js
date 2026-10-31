/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        bgPrimary: '#06090E',
        bgSecondary: '#090E17',
        bgSection: '#0B1220',
        cyanElectric: '#0EA5E9',
        cyanLight: '#38BDF8',
        emeraldLive: '#10B981',
        textPrimary: '#F8FAFC',
        textSecondary: '#94A3B8',
        textMuted: '#64748B',
      },
      fontFamily: {
        sans: ['"Plus Jakarta Sans"', 'Inter', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      boxShadow: {
        glowCyan: '0 0 35px -5px rgba(14, 165, 233, 0.25)',
        glowEmerald: '0 0 30px -5px rgba(16, 185, 129, 0.25)',
      }
    },
  },
  plugins: [],
}
