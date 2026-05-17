import json
import base64
import torch
import numpy as np
import joblib
import os
from io import BytesIO
from PIL import Image
from models import create_model

# ========================= CONFIG =========================
# Vercel stores model files in public/ directory or /tmp
MODEL_PATH = "public/models/Best_AlexNet.pth"
PCA_PATH = "public/models/pca_8components.pkl"
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
        try:
            if not os.path.exists(MODEL_PATH):
                return None, None, f"Model file not found at {MODEL_PATH}"
            
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
            
            return _model, _pca, None
        except Exception as e:
            return None, None, str(e)
    
    return _model, _pca, None

def preprocess_image(image_bytes):
    """Process image from various formats (PNG, JPG, etc.)"""
    try:
        img = Image.open(BytesIO(image_bytes))
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to 64x64
        img = img.resize((64, 64), Image.Resampling.LANCZOS)
        
        # Convert to numpy array
        img_array = np.array(img).astype(np.float32)
        
        # Convert to tensor (HxWxC -> CxHxW)
        img_tensor = torch.from_numpy(img_array).permute(2, 0, 1)
        
        # Normalize to [0, 1]
        img_tensor = img_tensor / 255.0
        
        # Expand RGB (3 channels) to 8 channels to match PCA input
        # Duplicate channels to simulate Sentinel-2 spectral bands
        channel_expanded = torch.cat([
            img_tensor,  # RGB: 3 channels
            img_tensor[0:1],  # R channel again
            img_tensor[1:2],  # G channel again
            img_tensor[2:3],  # B channel again
            img_tensor[0:1],  # R channel again
        ], dim=0)[:8]  # Take first 8 channels
        
        return channel_expanded
        
    except Exception as e:
        print(f"Image preprocessing error: {e}")
        return None

def handler(request):
    """Vercel serverless function handler"""
    
    # Handle CORS
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }
    
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': 'OK'})
        }
    
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'headers': headers,
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        # Parse JSON body
        body = json.loads(request.body) if isinstance(request.body, str) else request.body
        
        if 'image' not in body:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'No image data provided'})
            }
        
        # Decode base64 image
        image_data = body['image']
        if ',' in image_data:
            # Remove data URL prefix (e.g., "data:image/png;base64,")
            image_data = image_data.split(',')[1]
        
        try:
            image_bytes = base64.b64decode(image_data)
        except Exception as e:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': f'Invalid base64 image: {str(e)}'})
            }
        
        # Load model
        model, pca, error = load_model()
        if model is None:
            return {
                'statusCode': 503,
                'headers': headers,
                'body': json.dumps({'error': f'Model not available: {error}'})
            }
        
        # Preprocess image
        img_tensor = preprocess_image(image_bytes)
        if img_tensor is None:
            return {
                'statusCode': 400,
                'headers': headers,
                'body': json.dumps({'error': 'Failed to process image'})
            }
        
        # Apply PCA if available
        if pca is not None:
            img_np = img_tensor.numpy()  # (8, 64, 64)
            C, H, W = img_np.shape
            flat = img_np.reshape(C, -1).T  # (H*W, 8)
            reduced = pca.transform(flat)  # (H*W, 8)
            img_tensor = torch.from_numpy(reduced.T).float().reshape(-1, H, W)
        
        # Add batch dimension and move to device
        img_tensor = img_tensor.unsqueeze(0).to(DEVICE)
        
        # Run inference
        with torch.no_grad():
            outputs = model(img_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
        
        predicted_class = CLASSES[predicted.item()]
        confidence_score = float(confidence.item())
        
        # Get top 3 predictions
        top_probs, top_indices = torch.topk(probabilities[0], min(3, len(CLASSES)))
        top_predictions = [
            {
                'class': CLASSES[idx.item()],
                'confidence': float(prob.item())
            }
            for prob, idx in zip(top_probs, top_indices)
        ]
        
        response = {
            'predicted_class': predicted_class,
            'confidence': round(confidence_score * 100, 2),
            'top_predictions': top_predictions,
            'all_probabilities': {
                CLASSES[i]: round(float(probabilities[0][i].item()) * 100, 2)
                for i in range(len(CLASSES))
            }
        }
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(response)
        }
        
    except Exception as e:
        print(f"Handler error: {e}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': f'Server error: {str(e)}'})
        }
