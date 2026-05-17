'use client'

import { useState, useRef } from 'react'
import { formatProbabilities } from '@/lib/utils'

interface PredictionResult {
  predicted_class: string
  confidence: number
  probabilities: Record<string, number>
}

export default function Classifier() {
  const [file, setFile] = useState<File | null>(null)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<PredictionResult | null>(null)
  const [error, setError] = useState<string | null>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0]
    if (selectedFile) {
      if (!selectedFile.name.endsWith('.tif') && !selectedFile.name.endsWith('.tiff')) {
        setError('Only .tif files are supported')
        setFile(null)
        return
      }
      setFile(selectedFile)
      setError(null)
      setResult(null)
    }
  }

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    const droppedFile = e.dataTransfer.files?.[0]
    if (droppedFile) {
      if (!droppedFile.name.endsWith('.tif') && !droppedFile.name.endsWith('.tiff')) {
        setError('Only .tif files are supported')
        setFile(null)
        return
      }
      setFile(droppedFile)
      setError(null)
      setResult(null)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) {
      setError('Please select a file')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch('/api/classify', {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Classification failed')
      }

      const data = await response.json()
      setResult(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const classDescriptions: Record<string, string> = {
    AnnualCrop: 'Seasonal crops planted yearly',
    Forest: 'Dense vegetation and timber areas',
    HerbaceousVegetation: 'Grass and herbaceous plants',
    Highway: 'Major roads and highways',
    Industrial: 'Industrial facilities and factories',
    Pasture: 'Grazing land for livestock',
    PermanentCrop: 'Long-term crops (orchards, vineyards)',
    Residential: 'Urban residential areas',
    River: 'Freshwater rivers and streams',
    SeaLake: 'Bodies of salt and freshwater',
  }

  return (
    <div className="relative z-10 min-h-screen flex items-center justify-center px-4 py-12">
      <div className="w-full max-w-2xl">
        <div className="card space-y-8">
          {/* Header */}
          <div className="text-center space-y-2">
            <h1 className="text-4xl md:text-5xl font-orbitron font-bold text-gradient">
              LAND TYPE ANALYZER
            </h1>
            <p className="text-ice text-sm md:text-base font-rajdhani">
              Upload a Sentinel-2 satellite image (.tif) to classify the land type
            </p>
          </div>

          {/* Upload Area */}
          <form onSubmit={handleSubmit} className="space-y-6">
            <div
              onDrop={handleDrop}
              onDragOver={(e) => e.preventDefault()}
              className="border-2 border-dashed border-neon/50 rounded-lg p-8 text-center cursor-pointer
                hover:border-neon hover:bg-neon/5 transition-all duration-300 group"
              onClick={() => fileInputRef.current?.click()}
            >
              <input
                ref={fileInputRef}
                type="file"
                accept=".tif,.tiff"
                onChange={handleFileSelect}
                className="hidden"
              />

              <div className="space-y-4">
                <svg
                  className="mx-auto h-12 w-12 text-neon group-hover:text-ice transition-colors"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 4v16m8-8H4"
                  />
                </svg>

                {file ? (
                  <div className="space-y-2">
                    <p className="text-neon font-orbitron font-bold">{file.name}</p>
                    <p className="text-ice text-sm">
                      {(file.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                ) : (
                  <>
                    <p className="text-white font-rajdhani font-semibold">
                      Drag and drop your .tif file here
                    </p>
                    <p className="text-muted text-sm">or click to browse</p>
                  </>
                )}
              </div>
            </div>

            {/* Error Display */}
            {error && (
              <div className="bg-warn/10 border border-warn rounded-lg p-4 text-warn text-sm">
                <p className="font-rajdhani font-semibold">{error}</p>
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={!file || loading}
              className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <span className="flex items-center justify-center gap-2">
                  <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                      fill="none"
                    />
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    />
                  </svg>
                  CLASSIFYING...
                </span>
              ) : (
                'CLASSIFY IMAGE'
              )}
            </button>
          </form>

          {/* Results Display */}
          {result && (
            <div className="space-y-6 animate-fadeInUp">
              {/* Predicted Class */}
              <div className="bg-electric/10 border border-electric rounded-lg p-6 space-y-3">
                <p className="text-muted text-sm font-orbitron uppercase tracking-wider">
                  CLASSIFICATION RESULT
                </p>
                <h2 className="text-3xl md:text-4xl font-orbitron font-bold text-neon">
                  {result.predicted_class}
                </h2>
                <p className="text-ice text-sm">
                  {classDescriptions[result.predicted_class as keyof typeof classDescriptions]}
                </p>
                <div className="flex items-center gap-2">
                  <div className="flex-1 bg-deep border border-neon/30 rounded h-2">
                    <div
                      className="bg-gradient-to-r from-electric to-neon h-full rounded transition-all duration-500"
                      style={{ width: `${result.confidence}%` }}
                    />
                  </div>
                  <span className="text-neon font-orbitron font-bold text-lg">
                    {result.confidence.toFixed(1)}%
                  </span>
                </div>
              </div>

              {/* Probability Breakdown */}
              <div className="space-y-3">
                <h3 className="text-white font-orbitron font-bold uppercase tracking-wider text-sm">
                  Confidence Breakdown
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                  {Object.entries(result.probabilities)
                    .sort(([, a], [, b]) => b - a)
                    .map(([className, probability]) => (
                      <div key={className} className="space-y-1">
                        <div className="flex justify-between text-xs">
                          <span className="text-ice">{className}</span>
                          <span className="text-neon font-orbitron">
                            {probability.toFixed(1)}%
                          </span>
                        </div>
                        <div className="bg-deep border border-neon/20 rounded h-1.5">
                          <div
                            className="bg-gradient-to-r from-muted to-neon h-full rounded transition-all duration-500"
                            style={{ width: `${probability}%` }}
                          />
                        </div>
                      </div>
                    ))}
                </div>
              </div>

              {/* Reset Button */}
              <button
                onClick={() => {
                  setFile(null)
                  setResult(null)
                  setError(null)
                  if (fileInputRef.current) fileInputRef.current.value = ''
                }}
                className="btn-secondary w-full"
              >
                ANALYZE ANOTHER IMAGE
              </button>
            </div>
          )}
        </div>

        {/* Footer Info */}
        <div className="mt-8 text-center text-muted text-xs font-rajdhani">
          <p>Powered by AI • Uses Sentinel-2 satellite imagery for classification</p>
        </div>
      </div>
    </div>
  )
}
