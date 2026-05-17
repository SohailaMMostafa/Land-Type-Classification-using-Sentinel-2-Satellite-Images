# 🚀 Quick Start Guide

Get your Land Type Classification system running in 5 minutes!

## 1. Install & Run Locally

```bash
# Clone and install
npm install

# Start development server
npm run dev

# Open in browser
open http://localhost:3000
```

## 2. Add Model Files

Copy your trained models to:
```
public/models/
├── Best_AlexNet.pth
└── pca_8components.pkl
```

## 3. Test the System

1. Go to http://localhost:3000
2. Upload a Sentinel-2 satellite image (.tif format)
3. See instant classification results!

## 4. Deploy to Production

### Quick Deploy (1 command):
```bash
npm run deploy
```

### Or Manual Deploy:
```bash
# Login to Vercel
npm i -g vercel
vercel login

# Deploy
vercel deploy --prod
```

## 5. Share Your System

Once deployed, share the URL with your users:
```
https://your-project.vercel.app
```

---

**That's it! Your ORBIT system is live.** 🎉

For detailed setup instructions, see [DEPLOYMENT.md](./DEPLOYMENT.md)

### Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| "Model not found" | Add model files to `public/models/` |
| Port 3000 in use | Use `npm run dev -- -p 3001` |
| Build error | Run `npm install` again |
| Slow classification | Ensure Python dependencies installed |

### Key Files

- `app/page.tsx` - Main interface
- `components/Classifier.tsx` - Upload & results
- `app/api/classify/route.ts` - API endpoint
- `api/classify.py` - ML inference

### Next Steps

1. Customize branding in `components/Classifier.tsx`
2. Add more model options in `api/models.py`
3. Set up monitoring with Vercel Analytics
4. Consider adding user accounts & history
5. Optimize model size for faster loading

---

Questions? Check the [README.md](./README.md) for full documentation.
