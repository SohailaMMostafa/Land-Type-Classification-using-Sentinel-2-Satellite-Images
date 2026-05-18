# 🛰️ Land Type Classification using Sentinel-2 Satellite Images

This project develops a deep learning-based system to classify land types (e.g., AnnualCrop, Forest, Residential, River, etc.) from **Sentinel-2 satellite imagery**. It leverages the EuroSAT dataset (all bands) and explores multiple CNN architectures (AlexNet, ResNet, EfficientNet, GoogleNet), with hyperparameter tuning, PCA dimensionality reduction, visualizations, and a web interface for inference.

**Live Demo**: [land-type-classification.vercel.app](https://land-type-classification.vercel.app/)

## Project Overview

- **Dataset**: EuroSAT (Sentinel-2 patches with 13 spectral bands, 10 land cover classes).
- **Models**: CNNs including AlexNet, ResNet, EfficientNet, and GoogleNet.
- **Key Features**:
  - Multi-band image processing
  - Hyperparameter tuning and model selection
  - Dimensionality reduction with PCA
  - Spectral indices visualizations (NDVI, NDWI, NDBI)
  - Trained model inference via a simple web interface

---

## Repository Structure

### Root Files
- **`WorkFlow.pdf`** — Project workflow diagram and overall pipeline summary.<grok-card data-id="27e33d" data-type="citation_card" data-plain-type="render_inline_citation" ></grok-card>

### Folders

- **`.idea/`**  
  PyCharm / IntelliJ IDEA project configuration files (ignore for general use).

- **`EuroSATallBands/`**  
  The dataset organized by class folders: `AnnualCrop`, `Forest`, `HerbaceousVegetation`, `Highway`, `Industrial`, `Pasture`, `PermanentCrop`, `Residential`, `River`, `SeaLake`. Contains the raw Sentinel-2 image patches (all 13 bands).

- **`Interface/`**  
  Web inference interface.  
  - `Land Type Classification.html` — Main HTML frontend for the classifier.  
  - `dataset.py` — Data loading and preprocessing utilities.  
  - `inference_api.py` — Backend API for running predictions.  
  - `models.py` — Model definitions and loading for inference.

- **`Model Selection/`**  
  Core training and experimentation scripts.  
  - `PCA.py` / `PCA_CODE.ipynb` — Principal Component Analysis for band reduction.  
  - `dataset.py` — Dataset handling and loading.  
  - `hyperparameter_tuning.py` — Hyperparameter search.  
  - `models.py` — Model architectures (AlexNet, ResNet, etc.).  
  - `train.py` — General training script.  
  - `train_AlexNet_gpu.py`, `train_Efficientnet_gpu.py`, `train_GoogleNet_gpu.py`, `train_ResNet_gpu.py` — GPU-optimized training scripts for each architecture.

- **`models/`**  
  Saved trained models and related artifacts.  
  - `Best_AlexNet.pth`, `best_hyperparams.pth` — Best performing model weights.  
  - `pca_8components.pkl` — Fitted PCA transformer.  
  - `Hyperpaeams tuning.png` — Visualization of hyperparameter results.

- **`results/`**  
  Training outputs, metrics, and evaluation plots.  
  - `.png` and `.txt` files for each model (e.g., `AlexNet (1).png`, `ResNet (1).txt`) containing accuracy curves, confusion matrices, classification reports, etc.

- **`visualizations/`**  
  Exploratory data analysis and spectral visualizations.  
  - `Source Code.ipynb` — Jupyter notebook with visualization code.  
  - `Orignal_Functions.py` — Helper functions for plotting.  
  - `sample_images_rgb.png`, `sample_images_false_color.png` — Example patches.  
  - `ndvi_maps.png`, `ndwi_maps.png`, `ndbi_maps.png` — Spectral index maps.  
  - `spectral_signatures.png` — Average spectral signatures per class.

---

## How to Use

1. **Explore Data & Visualizations** → Check `visualizations/` and `EuroSATallBands/`.
2. **Reproduce Training** → Run scripts in `Model Selection/`.
3. **Inference** → Use the `Interface/` folder (open the HTML or run the API).
4. **Pre-trained Models** → Available in the `models/` folder.

## Technologies

- Python, PyTorch
- Jupyter Notebooks
- HTML + Python backend for interface
- scikit-learn (PCA), Matplotlib/Seaborn

## License

Open source (feel free to use and contribute).

---

**Made with ❤️ for Earth Observation & Deep Learning**
