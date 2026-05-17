# 🚀 Deployment Guide for ORBIT

Complete guide to deploy your Land Type Classification system to production.

## Prerequisites

- GitHub account with your repo pushed
- Vercel account (free tier available)
- Model files ready (Best_AlexNet.pth, pca_8components.pkl)

## Step 1: Prepare Your Repository

### Local Setup

```bash
# Install dependencies
npm install

# Test locally
npm run dev

# Build for production
npm run build

# Commit everything
git add .
git commit -m "Ready for production deployment"
git push origin main
```

## Step 2: Set Up Vercel Project

### Option A: Connect GitHub (Recommended)

1. Go to [vercel.com/new](https://vercel.com/new)
2. Select "Import Git Repository"
3. Search for your repo: `SohailaMMostafa/Land-Type-Classification-using-Sentinel-2-Satellite-Images`
4. Click "Import"
5. Configure project:
   - **Project Name**: `land-type-classifier`
   - **Framework Preset**: Next.js
   - **Root Directory**: `.` (default)
6. Click "Deploy"

### Option B: Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Login
vercel login

# Deploy (in project directory)
vercel

# Follow prompts to link/create project
```

## Step 3: Configure Model Files

### Method 1: Store in Public Folder (Small Models)

```bash
# Create models directory
mkdir -p public/models

# Copy model files (from your local training)
cp Best_AlexNet.pth public/models/
cp pca_8components.pkl public/models/

# Commit
git add public/models/
git commit -m "Add model files"
git push
```

⚠️ **Note**: Model files are large. Keep in mind Vercel's deployment limits.

### Method 2: Use Vercel Blob Storage (Recommended)

1. Install Blob integration:
   ```bash
   vercel env pull
   ```

2. Add to your Vercel project settings:
   - Go to Settings → Integrations
   - Add "Blob" integration
   - Copy the BLOB_READ_WRITE_TOKEN

3. Update environment variables:
   ```bash
   vercel env add BLOB_READ_WRITE_TOKEN
   # Paste your token
   ```

4. Update `api/classify.py` to load from Blob:
   ```python
   import requests
   from vercel_blob import get_blob_download_url
   
   # Download model at startup
   model_url = get_blob_download_url("Best_AlexNet.pth")
   response = requests.get(model_url)
   ```

### Method 3: Use AWS S3

1. Create S3 bucket with model files
2. Add environment variables:
   ```bash
   vercel env add AWS_ACCESS_KEY_ID
   vercel env add AWS_SECRET_ACCESS_KEY
   vercel env add AWS_S3_BUCKET
   ```

3. Update `api/classify.py`:
   ```python
   import boto3
   
   s3 = boto3.client('s3', 
       aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
       aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
   )
   s3.download_file(os.getenv('AWS_S3_BUCKET'), 'Best_AlexNet.pth', '/tmp/Best_AlexNet.pth')
   ```

## Step 4: Set Environment Variables

In your Vercel project dashboard:

1. Go to **Settings** → **Environment Variables**
2. Add these variables:

```
VERCEL_URL=your-domain.vercel.app
MODEL_PATH=/tmp/Best_AlexNet.pth
PCA_PATH=/tmp/pca_8components.pkl
```

## Step 5: Configure Python Runtime

Update `vercel.json`:

```json
{
  "buildCommand": "npm run build",
  "framework": "nextjs",
  "functions": {
    "api/classify.py": {
      "runtime": "python3.12",
      "memory": 3008,
      "maxDuration": 60
    }
  }
}
```

## Step 6: Deploy

### Auto-Deploy (GitHub Connected)

Every push to your repo automatically triggers deployment:

```bash
git add .
git commit -m "Update configuration"
git push origin main
```

Monitor deployment in Vercel dashboard → Deployments tab.

### Manual Deployment

```bash
vercel deploy --prod
```

## Step 7: Monitor & Test

### Check Deployment Status

1. Visit Vercel Dashboard
2. Click on your project
3. Go to Deployments → Click latest deployment
4. Check build logs for errors

### Test the API

```bash
# Get your deployment URL from Vercel
# Example: https://land-type-classifier.vercel.app

# Test upload
curl -X POST https://land-type-classifier.vercel.app/api/classify \
  -F "file=@test_image.tif"
```

### View Live App

```
https://land-type-classifier.vercel.app
```

## Troubleshooting

### "Module not found: torch"

**Solution**: Python dependencies must be declared in `requirements.txt`:

```bash
cat > requirements.txt << EOF
torch>=2.0.0
torchvision>=0.15.0
numpy>=1.24.0
rasterio>=1.3.0
joblib>=1.3.0
pillow>=10.0.0
EOF

git add requirements.txt
git push
vercel deploy --prod
```

### "Model files not found"

**Solutions**:
- Check model files are in correct location
- Verify file permissions (public folder is readable)
- Use cloud storage instead of local files
- Download on cold start from external source

### "502 Bad Gateway"

**Causes & Solutions**:
- Function timeout (increase maxDuration to 60s)
- Out of memory (ensure 3008MB allocation)
- Model file loading error (check logs)

**Check logs**:
```bash
vercel logs <project-url>
```

### "Build failed"

**Solutions**:
- Check npm dependencies
- Verify all imports exist
- Test build locally first: `npm run build`
- Check `next.config.js` for syntax errors

## Performance Optimization

### Reduce Model Size

Train a smaller model or use quantization:

```python
# In training script
torch.jit.script(model)  # JIT compilation
model = torch.quantization.quantize_dynamic(model, {torch.nn.Linear}, dtype=torch.qint8)
torch.save(model, 'model_quantized.pth')
```

### Cache Model Loading

Model is cached on first request. Subsequent requests reuse it:

```python
# api/classify.py already implements caching
_model = None  # Global cache
_pca = None

def load_model():
    global _model, _pca
    if _model is None:
        # Load once
```

### Enable Vercel Analytics

In Vercel dashboard → Analytics tab:
- Monitor function execution time
- Track cold starts
- Identify bottlenecks

## Scaling Configuration

### For High Traffic

1. Increase function memory (up to 3008MB in free tier)
2. Set `maxDuration` to 60 seconds
3. Use persistent storage for models (Blob/S3)
4. Consider Vercel Pro for better scaling

```json
{
  "functions": {
    "api/classify.py": {
      "memory": 3008,
      "maxDuration": 60
    }
  }
}
```

### Cost Estimates

- **Free Tier**: 150 minutes/month execution time
- **Pro**: Pay per use (~$0.50 per GB-hour)
- **Enterprise**: Custom pricing

## Rollback

If deployment has issues:

```bash
# Revert to previous deployment
vercel rollback
```

Or select previous deployment in dashboard and click "Promote to Production".

## Custom Domain

1. In Vercel dashboard → Settings → Domains
2. Add your domain (e.g., classify.earth)
3. Update DNS records according to Vercel's instructions
4. SSL certificate auto-provisioned

## Success Checklist

- [ ] GitHub repo connected
- [ ] Dependencies installed
- [ ] Model files accessible
- [ ] Environment variables set
- [ ] Build successful
- [ ] API responding to requests
- [ ] Frontend loads and works
- [ ] Classification results displaying
- [ ] Monitoring/logs configured
- [ ] Custom domain active (optional)

## Next Steps

1. **Monitor Analytics**: Track usage patterns
2. **Gather User Feedback**: Improve UX
3. **Fine-tune Models**: Train on more data
4. **Add Features**: Batch processing, history, exports
5. **Scale Infrastructure**: Upgrade as needed

---

**Deployment complete! Your ORBIT system is live! 🎉**

Questions? Check:
- [Vercel Docs](https://vercel.com/docs)
- [Next.js Docs](https://nextjs.org/docs)
- [PyTorch Docs](https://pytorch.org/docs)
