import { NextRequest, NextResponse } from 'next/server';

export async function OPTIONS(request: NextRequest) {
  return NextResponse.json(
    { message: 'OK' },
    {
      status: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
      },
    }
  );
}

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const file = formData.get('file');

    if (!file || !(file instanceof File)) {
      return NextResponse.json(
        { detail: 'No file provided' },
        { status: 400, headers: { 'Access-Control-Allow-Origin': '*' } }
      );
    }

    // Convert file to base64
    const bytes = await file.arrayBuffer();
    const buffer = Buffer.from(bytes);
    const base64 = buffer.toString('base64');

    // Call the Python serverless function
    const pythonResponse = await fetch(
      process.env.VERCEL_URL
        ? `https://${process.env.VERCEL_URL}/api/classify`
        : 'http://localhost:3000/api/classify',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image: `data:image/${file.type};base64,${base64}`,
        }),
      }
    );

    if (!pythonResponse.ok) {
      const error = await pythonResponse.json();
      return NextResponse.json(
        { detail: error.error || 'Prediction failed' },
        { status: pythonResponse.status, headers: { 'Access-Control-Allow-Origin': '*' } }
      );
    }

    const result = await pythonResponse.json();
    return NextResponse.json(result, {
      status: 200,
      headers: { 'Access-Control-Allow-Origin': '*' },
    });
  } catch (error) {
    console.error('API error:', error);
    return NextResponse.json(
      { detail: `Error: ${error instanceof Error ? error.message : 'Unknown error'}` },
      { status: 500, headers: { 'Access-Control-Allow-Origin': '*' } }
    );
  }
}
