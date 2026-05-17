import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        void: '#010812',
        abyss: '#030e20',
        deep: '#061628',
        navy: '#0a2040',
        steel: '#0d2d56',
        azure: '#1255a8',
        electric: '#1a7fff',
        neon: '#00d4ff',
        ice: '#a8e8ff',
        muted: '#3a6a9a',
        faint: '#1a3a5c',
        glow: '#00ff9d',
        warn: '#ffb800',
      },
      fontFamily: {
        rajdhani: ['Rajdhani', 'sans-serif'],
        orbitron: ['Orbitron', 'sans-serif'],
        'share-tech': ['Share Tech Mono', 'monospace'],
      },
      backgroundImage: {
        grid: 'linear-gradient(rgba(0, 212, 255, 0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 212, 255, 0.04) 1px, transparent 1px)',
      },
      backgroundSize: {
        grid: '50px 50px',
      },
    },
  },
  plugins: [],
}
export default config
