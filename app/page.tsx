import Starfield from '@/components/Starfield'
import Classifier from '@/components/Classifier'

export default function Home() {
  return (
    <main className="relative min-h-screen w-full bg-void">
      {/* Background Elements */}
      <Starfield />
      <div className="grid-overlay" />

      {/* Orbital Rings */}
      <div className="orbital-ring or1" />
      <div className="orbital-ring or2" />
      <div className="orbital-ring or3" />

      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 h-16 bg-void/92 border-b border-neon/10 backdrop-blur-md">
        <div className="h-full px-4 md:px-8 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full border-2 border-neon flex items-center justify-center">
              <div className="w-4 h-4 rounded-full bg-neon/50" />
            </div>
            <h1 className="text-xl md:text-2xl font-orbitron font-bold text-gradient hidden sm:block">
              ORBIT
            </h1>
          </div>
          <p className="text-xs md:text-sm text-muted font-rajdhani">
            Earth Intelligence Platform
          </p>
        </div>
      </nav>

      {/* Main Content */}
      <div className="pt-16">
        <Classifier />
      </div>
    </main>
  )
}
