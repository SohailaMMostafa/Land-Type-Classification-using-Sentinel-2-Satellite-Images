import type { Metadata, Viewport } from 'next'
import './globals.css'

const metadata: Metadata = {
  title: 'ORBIT — Earth Intelligence',
  description: 'EuroSAT Land Type Classification using Sentinel-2 Satellite Images',
  keywords: 'satellite, classification, sentinel-2, machine learning, earth intelligence',
  openGraph: {
    title: 'ORBIT — Earth Intelligence',
    description: 'Advanced land type classification using satellite imagery',
  },
}

const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
}

export { metadata, viewport }

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link
          href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&family=Orbitron:wght@400;500;700;900&family=Share+Tech+Mono&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="bg-void text-white overflow-x-hidden font-rajdhani cursor-crosshair">
        {children}
      </body>
    </html>
  )
}
