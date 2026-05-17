# 🛰️ ORBIT — Earth Intelligence Platform

Advanced land type classification system using Sentinel-2 satellite imagery and deep learning.

## Features

- **State-of-the-art Classification**: Uses AlexNet trained on EuroSAT dataset
- **10 Land Types**: AnnualCrop, Forest, Herbaceous Vegetation, Highway, Industrial, Pasture, Permanent Crop, Residential, River, SeaLake
- **Real-time Processing**: Fast inference on uploaded satellite images
- **Beautiful Interface**: Futuristic ORBIT-themed UI with smooth animations
- **Production Ready**: Deployed on Vercel serverless platform

## Tech Stack

- **Frontend**: Next.js 15, React 18, Tailwind CSS
- **Backend**: Python, PyTorch, FastAPI (Vercel Functions)
- **Deployment**: Vercel
- **ML Models**: AlexNet, PCA (8 components)

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.11+
- npm or yarn

### Local Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Open browser
open http://localhost:3000
```

### Build for Production

```bash
npm run build
npm start
```

## Deployment on Vercel

### Option 1: Via GitHub (Recommended)

1. Push to your GitHub repository
2. Connect repository to Vercel in project settings
3. Vercel auto-deploys on every push

### Option 2: Via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

## Model Files

The classification requires two model files:

1. **Best_AlexNet.pth** - PyTorch model weights
2. **pca_8components.pkl** - PCA transformer

### Setting Up Model Files

Place these files in your project:

```
/public/models/
├── Best_AlexNet.pth
└── pca_8components.pkl
```

**Production Deployment**:
- Store model files in Vercel Blob storage or AWS S3
- Update `api/classify.py` to download from cloud storage
- Add environment variables for storage credentials

## API Endpoints

### POST `/api/classify`

Classify a satellite image.

**Request**:
```bash
curl -X POST http://localhost:3000/api/classify \
  -F "file=@satellite_image.tif"
```

**Response**:
```json
{
  "predicted_class": "Forest",
  "confidence": 92.5,
  "probabilities": {
    "AnnualCrop": 2.1,
    "Forest": 92.5,
    "HerbaceousVegetation": 1.3,
    ...
  }
}
```

## Environment Variables

```env
# Required for production
VERCEL_URL=your-domain.vercel.app

# Optional: Cloud storage (if using external model storage)
MODEL_STORAGE_URL=https://your-storage.com
```

## Architecture

```
┌─────────────────────────────────────────┐
│         Browser (Next.js Frontend)      │
│  - React Components                     │
│  - Tailwind CSS Styling                 │
│  - File Upload & Results Display        │
└──────────────┬──────────────────────────┘
               │ POST /api/classify
               ↓
┌─────────────────────────────────────────┐
│    Vercel Serverless (Node.js)          │
│  - API Route Handler                    │
│  - Form Data Processing                 │
└──────────────┬──────────────────────────┘
               │ Call Python Function
               ↓
┌─────────────────────────────────────────┐
│   Vercel Python Function                │
│  - PyTorch Model Loading                │
│  - Image Preprocessing (PCA)            │
│  - Inference & Classification           │
│  - Results JSON Response                │
└─────────────────────────────────────────┘
```

## Performance

- **Processing Time**: ~2-5 seconds per image
- **Model Size**: ~250MB (AlexNet + PCA)
- **Memory Required**: 3GB (Vercel Functions: 3008MB)
- **Concurrent Requests**: Serverless auto-scaling

## Land Type Categories

| Class | Description |
|-------|------------|
| **AnnualCrop** | Seasonal crops planted yearly |
| **Forest** | Dense vegetation and timber areas |
| **HerbaceousVegetation** | Grass and herbaceous plants |
| **Highway** | Major roads and highways |
| **Industrial** | Industrial facilities and factories |
| **Pasture** | Grazing land for livestock |
| **PermanentCrop** | Long-term crops (orchards, vineyards) |
| **Residential** | Urban residential areas |
| **River** | Freshwater rivers and streams |
| **SeaLake** | Bodies of salt and freshwater |

## Troubleshooting

### "Model files not found"
- Ensure model files are in `/public/models/`
- On Vercel, configure cloud storage access

### "Only .tif files are supported"
- Input files must be Sentinel-2 satellite images in GeoTIFF format
- Ensure images are 64×64 pixels with 13 bands

### Slow inference
- Check Vercel function memory allocation (should be 3008MB)
- Monitor cold starts with Vercel Analytics

## Future Improvements

- [ ] Batch processing support
- [ ] API key authentication
- [ ] Result history and analytics
- [ ] Custom model fine-tuning
- [ ] Multi-temporal analysis
- [ ] Download classification reports

## License

Proprietary - All rights reserved

## Support

For issues or questions:
1. Check Vercel documentation
2. Review project settings
3. Contact support@vercel.com

---

**Built with ❤️ for Earth Intelligence**
