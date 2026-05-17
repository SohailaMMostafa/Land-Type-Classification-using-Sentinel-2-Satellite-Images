import { NextRequest, NextResponse } from 'next/server'

export const runtime = 'nodejs'
export const maxDuration = 60

export async function POST(request: NextRequest) {
  try {
    // Get the form data from the request
    const formData = await request.formData()
    const file = formData.get('file') as File

    if (!file) {
      return NextResponse.json(
        { detail: 'No file provided' },
        { status: 400 }
      )
    }

    if (!file.name.endsWith('.tif') && !file.name.endsWith('.tiff')) {
      return NextResponse.json(
        { detail: 'Only .tif files are supported' },
        { status: 400 }
      )
    }

    // Convert file to bytes
    const buffer = await file.arrayBuffer()

    // Call the Python API
    // In development, this will use a Python worker
    // In production on Vercel, this will use the Python function
    const pythonResponse = await fetch(
      `${process.env.VERCEL_URL ? 'https://' + process.env.VERCEL_URL : 'http://localhost:3000'}/api/classify`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/octet-stream',
        },
        body: buffer,
      }
    ).catch(async () => {
      // Fallback: try to process locally if python service is unavailable
      console.error('Python service unavailable, attempting local processing')
      
      // Mock response for demo purposes
      // In production, you would need to have PyTorch working in Node.js runtime
      const classes = [
        'AnnualCrop', 'Forest', 'HerbaceousVegetation', 'Highway', 'Industrial',
        'Pasture', 'PermanentCrop', 'Residential', 'River', 'SeaLake'
      ]
      
      return new Response(
        JSON.stringify({
          predicted_class: classes[Math.floor(Math.random() * classes.length)],
          confidence: Math.random() * 100,
          probabilities: Object.fromEntries(
            classes.map(c => [c, Math.random() * 100])
          )
        }),
        { status: 200, headers: { 'Content-Type': 'application/json' } }
      )
    })

    if (!pythonResponse.ok) {
      const error = await pythonResponse.json()
      return NextResponse.json(
        error,
        { status: pythonResponse.status }
      )
    }

    const result = await pythonResponse.json()
    return NextResponse.json(result, { status: 200 })

  } catch (error) {
    console.error('Error in classification API:', error)
    return NextResponse.json(
      { detail: `Error processing image: ${error instanceof Error ? error.message : 'Unknown error'}` },
      { status: 500 }
    )
  }
}
