import json
import torch
import rasterio
import numpy as np
import joblib
import os
from io import BytesIO
from models import create_model

# ========================= CONFIG =========================
MODEL_PATH = "/tmp/Best_AlexNet.pth"
PCA_PATH = "/tmp/pca_8components.pkl"
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Class names (must match your dataset order)
CLASSES = [
    "AnnualCrop", "Forest", "HerbaceousVegetation", "Highway", "Industrial",
    "Pasture", "PermanentCrop", "Residential", "River", "SeaLake"
]

# Global model and PCA (cached)
_model = None
_pca = None

def load_model():
    """Load model once on first request"""
    global _model, _pca
    
    if _model is None:
        # Download model files if not present
        if not os.path.exists(MODEL_PATH):
            print("[v0] Downloading model files...")
            # In production, you'd download from cloud storage
            # For now, we'll handle missing files gracefully
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
        
        # Load PCA
        _pca = joblib.load(PCA_PATH)
        print(f"✅ PCA loaded ({_pca.n_components_} components)")
        
        # Load Model
        _model = create_model(num_classes=10, in_channels=8, model_name='alexnet', pretrained=False)
        state_dict = torch.load(MODEL_PATH, map_location=DEVICE, weights_only=True)
        _model.load_state_dict(state_dict)
        _model.to(DEVICE)
        _model.eval()
        print(f"✅ Model loaded on {DEVICE}")
    
    return _model, _pca

def preprocess_tif(file_bytes):
    """Process uploaded .tif file"""
    with rasterio.MemoryFile(file_bytes) as memfile:
        with memfile.open() as src:
            img = src.read()  # (13, 64, 64)

    img = torch.from_numpy(img.astype(np.float32))

    # Same normalization as in training
    mean = img.mean(dim=(1, 2), keepdim=True)
    std = img.std(dim=(1, 2), keepdim=True) + 1e-8
    img = (img - mean) / std

    # Apply PCA
    model, pca = load_model()
    C, H, W = img.shape
    flat = img.reshape(C, -1).T.numpy()  # (H*W, 13)
    reduced = pca.transform(flat)  # (H*W, 8)
    reduced_img = torch.from_numpy(reduced.T).float().reshape(-1, H, W)

    # Add batch dimension
    return reduced_img.unsqueeze(0).to(DEVICE)  # (1, 8, 64, 64)

def handler(request):
    """Handler for Vercel serverless function"""
    
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        # Get file from request
        if 'file' not in request.files:
            return {
                'statusCode': 400,
                'body': json.dumps({'detail': 'No file provided'})
            }
        
        file = request.files['file']
        if file.filename == '':
            return {
                'statusCode': 400,
                'body': json.dumps({'detail': 'No file selected'})
            }
        
        if not file.filename.endswith(('.tif', '.tiff')):
            return {
                'statusCode': 400,
                'body': json.dumps({'detail': 'Only .tif files are supported'})
            }
        
        # Read file bytes
        file_bytes = file.read()
        
        # Preprocess
        input_tensor = preprocess_tif(file_bytes)
        
        # Load model and inference
        model, _ = load_model()
        
        with torch.no_grad():
            outputs = model(input_tensor)
            probabilities = torch.softmax(outputs[0], dim=0)
            predicted_idx = torch.argmax(probabilities).item()
            confidence = probabilities[predicted_idx].item() * 100
        
        predicted_class = CLASSES[predicted_idx]
        
        response = {
            "predicted_class": predicted_class,
            "confidence": round(confidence, 2),
            "probabilities": {
                CLASSES[i]: round(probabilities[i].item() * 100, 2)
                for i in range(10)
            }
        }
        
        return {
            'statusCode': 200,
            'body': json.dumps(response),
            'headers': {
                'Content-Type': 'application/json',
            }
        }
        
    except FileNotFoundError as e:
        return {
            'statusCode': 503,
            'body': json.dumps({'detail': f'Model files not found. Please ensure model files are configured: {str(e)}'})
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'detail': f'Error processing image: {str(e)}'})
        }
