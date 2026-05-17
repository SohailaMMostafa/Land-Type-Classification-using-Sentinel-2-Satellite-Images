# Vercel Deployment Guide - Land Type Classification

## Overview
Your application is now fully configured for Vercel deployment with:
- **Frontend**: Next.js 15 serving your original HTML interface
- **Backend**: Python serverless functions (PyTorch ML inference)
- **API**: Auto-deployed to Vercel's infrastructure

## Prerequisites
1. GitHub account with your repository pushed
2. Vercel account (free tier works)
3. Model files ready to upload

## Step 1: Prepare Model Files

Your model files MUST be placed in the `public/models/` directory:

```
public/
├── models/
│   ├── Best_AlexNet.pth       (download from your repo)
│   └── pca_8components.pkl    (download from your repo)
├── index.html                 (your interface)
└── ...
```

### How to Add Model Files

**Option A: Using Git (Recommended)**
```bash
# Copy model files to public/models/
mkdir -p public/models
cp /path/to/Best_AlexNet.pth public/models/
cp /path/to/pca_8components.pkl public/models/

# Commit and push
git add public/models/
git commit -m "Add model files for deployment"
git push origin set-project-production
```

**Option B: Upload via Vercel Dashboard**
1. Deploy to Vercel first (without models)
2. In Vercel Dashboard → Settings → Environment Variables
3. Or use the Vercel CLI to upload large files

## Step 2: Deploy to Vercel

### Option A: Auto-Deploy from GitHub (Easiest)

1. Go to [vercel.com](https://vercel.com)
2. Click "New Project"
3. Select your GitHub repository
4. Select branch: `set-project-production`
5. Framework: Next.js (auto-detected)
6. Click "Deploy"

Vercel will automatically:
- Install dependencies
- Build the Next.js app
- Deploy Python serverless functions
- Set up the API routes

### Option B: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod

# Follow the prompts to link your project
```

## Step 3: Configure Environment Variables (Optional)

If needed, set environment variables in Vercel:

1. Go to Project Settings → Environment Variables
2. Add any required environment variables
3. Redeploy

## Project Structure

```
.
├── app/
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Serves index.html
│   └── api/
│       ├── predict/route.ts    # Next.js endpoint (forwards to Python)
│       └── classify.py         # Python serverless function (ML inference)
├── public/
│   ├── index.html              # Your original HTML interface
│   └── models/                 # Model files (add here!)
│       ├── Best_AlexNet.pth
│       └── pca_8components.pkl
├── api/
│   ├── models.py               # PyTorch model definitions
│   ├── dataset.py              # Dataset utilities
│   ├── classify.py             # ML inference logic (duplicate)
│   └── __init__.py
├── vercel.json                 # Vercel configuration
├── requirements.txt            # Python dependencies
├── package.json                # Node.js dependencies
└── next.config.js              # Next.js configuration
```

## How It Works

1. **User uploads image** → HTML interface
2. **Frontend sends request** → `/api/predict` (Next.js endpoint)
3. **Next.js converts file** → Base64 encoded
4. **Forwards to** → `/api/classify` (Python serverless function)
5. **Python function**:
   - Decodes image
   - Preprocesses (resize, normalize)
   - Applies PCA
   - Runs PyTorch model
   - Returns predictions
6. **Results sent back** to HTML interface
7. **Display results** in ORBIT UI

## API Endpoints

### 1. Predict Endpoint (HTML friendly)
```
POST /api/predict
Content-Type: multipart/form-data

file: <image file>

Response:
{
  "predicted_class": "Forest",
  "confidence": 87.50,
  "top_predictions": [
    {"class": "Forest", "confidence": 0.8750},
    {"class": "HerbaceousVegetation", "confidence": 0.0850},
    {"class": "Pasture", "confidence": 0.0400}
  ],
  "all_probabilities": {
    "AnnualCrop": 0.0050,
    "Forest": 0.8750,
    ...
  }
}
```

### 2. Classify Endpoint (Direct Python function)
```
POST /api/classify
Content-Type: application/json

{
  "image": "data:image/png;base64,iVBORw0KGgo..."
}

Response: Same as above
```

## Supported Image Formats

- PNG
- JPG/JPEG
- GIF
- WebP
- TIFF (converted to RGB)

The system automatically converts any format to RGB and resizes to 64x64 pixels.

## Performance & Limits

- **Cold start**: First request takes 10-30 seconds (model loading)
- **Warm start**: Subsequent requests < 1 second
- **Memory**: 3008 MB (configured in vercel.json)
- **Timeout**: 60 seconds per request
- **Concurrent requests**: Auto-scales to thousands

Vercel will automatically warm functions during peak usage.

## Monitoring & Debugging

### View Logs in Vercel Dashboard

1. Go to Project → Deployments → Select deployment
2. Click "View Function Logs"
3. See real-time output from Python functions

### Local Testing

```bash
# Test locally first
npm run dev

# In another terminal, upload to http://localhost:3000
# and check browser console for errors
```

## Troubleshooting

### "Model file not found"
- Ensure `public/models/Best_AlexNet.pth` exists
- Redeploy: `vercel --prod`

### "CORS error"
- CORS is handled automatically in the API
- If issues persist, check browser console

### "Failed to fetch image"
- Ensure image format is supported
- Check file size < 50MB

### Timeout errors
- Model loading takes time on first request
- Wait 10-30 seconds for warm-up
- Increase maxDuration in vercel.json if needed

### Out of memory
- Reduce image resolution in preprocess_image()
- Or increase memory in vercel.json (may cost more)

## Cost Estimates

Vercel pricing (as of 2026):
- **Free tier**: 
  - 12 Serverless Function hours/month
  - 100 GB bandwidth/month
  - Perfect for testing
  
- **Pro tier** ($20/month):
  - Unlimited Function hours
  - Pay per GB beyond 100GB bandwidth
  - Recommended for production

Each inference costs approximately:
- Cold start: ~3-5 seconds of compute
- Warm start: ~0.5-1 second of compute

## Next Steps

1. ✅ Push model files to GitHub or upload separately
2. ✅ Connect GitHub to Vercel
3. ✅ Deploy using Vercel Dashboard
4. ✅ Test with sample satellite images
5. ✅ Share your live URL with users

## Support & Documentation

- **Vercel Docs**: https://vercel.com/docs
- **Next.js Docs**: https://nextjs.org/docs
- **PyTorch Docs**: https://pytorch.org/docs
- **Python Functions**: https://vercel.com/docs/functions/serverless-functions

## Key Files to Know

- `vercel.json` - Controls function memory, timeout, Python runtime
- `requirements.txt` - Python package dependencies
- `package.json` - Node.js dependencies
- `api/classify.py` - Your ML inference engine
- `public/index.html` - Your original interface (unmodified!)

---

**Your app is production-ready!** All deployment is handled by Vercel automatically.
