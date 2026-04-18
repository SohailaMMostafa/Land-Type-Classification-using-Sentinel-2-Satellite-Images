# Milestone 1: Exploratory Data Analysis & Data Preprocessing

## Overview
This milestone focuses on understanding the Sentinel-2 satellite image dataset and preparing it for machine learning model development. It includes comprehensive EDA, visualization analysis, vegetation index calculations, and data preprocessing.

## Objectives
- ✅ Perform exploratory data analysis (EDA) on the EuroSAT dataset with all Sentinel-2 bands
- ✅ Visualize sample images from different land types
- ✅ Examine spectral signatures of different land types
- ✅ Calculate vegetation indices (NDVI, NDBI, NDWI) for land type differentiation
- ✅ Apply data preprocessing (atmospheric correction, normalization)
- ✅ Split dataset into training, validation, and testing sets
- ✅ Create comprehensive visualizations and statistical analysis

## Dataset Description

### EuroSAT Dataset (Balanced Version)
- **Total Images**: 20,000 (2,000 images per land type - **perfectly balanced**)
- **Image Format**: GeoTIFF (.tif) with all 12 Sentinel-2 bands
- **Image Resolution**: 64 × 64 pixels
- **Spectral Bands**: 12 (see below)
- **Data Location**: `./Balanced data/` (inside milestone1 folder)

### Key Advantage of Balanced Dataset
✅ **Equal representation** - Each class has exactly 2,000 images
✅ **No class imbalance issues** - Avoids bias in model training
✅ **Faster processing** - 25% fewer images than full dataset
✅ **Fair evaluation** - Equal validation/test sets per class

### Land Type Classes
All classes have exactly **2,000 images** in the balanced dataset:

1. **AnnualCrop** (2,000) - Cropland with annual vegetation
2. **Forest** (2,000) - Forested areas
3. **HerbaceousVegetation** (2,000) - Grassland, herbaceous areas
4. **Highway** (2,000) - Road infrastructure
5. **Industrial** (2,000) - Industrial areas
6. **Pasture** (2,000) - Pastureland
7. **PermanentCrop** (2,000) - Perennial crops (vineyards, orchards)
8. **Residential** (2,000) - Residential/urban areas
9. **River** (2,000) - River/water bodies
10. **SeaLake** (2,000) - Sea and lake water

### Sentinel-2 Bands

| Band # | Name | Wavelength (nm) | Resolution (m) | Use |
|--------|------|-----------------|-----------------|-----|
| B1 | Coastal Aerosol | 443 | 60 | Atmospheric correction |
| B2 | Blue | 490 | 10 | Water penetration, soil |
| B3 | Green | 560 | 10 | RGB composite |
| B4 | Red | 665 | 10 | RGB composite, NDVI |
| B5 | Red Edge 1 | 705 | 20 | Vegetation stress |
| B6 | Red Edge 2 | 740 | 20 | Vegetation assessment |
| B7 | Red Edge 3 | 783 | 20 | Vegetation mapping |
| B8 | NIR | 842 | 10 | Vegetation monitoring, NDVI |
| B8A | Narrow NIR | 865 | 20 | Vegetation analysis |
| B9 | Water Vapor | 945 | 60 | Water vapor correction |
| B11 | SWIR 1 | 1610 | 20 | Built-up areas, NDBI |
| B12 | SWIR 2 | 2190 | 20 | Built-up areas, moisture |

## Key Vegetation Indices Calculated

### 1. NDVI (Normalized Difference Vegetation Index)
- **Formula**: `NDVI = (NIR - Red) / (NIR + Red)`
- **Purpose**: Quantifies vegetation greenness
- **Range**: -1 to +1
  - Negative values: Water
  - 0-0.2: Minimal vegetation
  - 0.2-0.5: Low to moderate vegetation
  - 0.5+: Dense vegetation

### 2. NDBI (Normalized Difference Built-up Index)
- **Formula**: `NDBI = (SWIR - NIR) / (SWIR + NIR)`
- **Purpose**: Identifies built-up areas and urban regions
- **Range**: -1 to +1
  - Positive values: Built-up areas
  - Negative values: Vegetation/water

### 3. NDWI (Normalized Difference Water Index)
- **Formula**: `NDWI = (NIR - SWIR) / (NIR + SWIR)`
- **Purpose**: Water detection and moisture assessment
- **Range**: -1 to +1
  - High positive values: Water bodies
  - Negative values: Dry vegetation

## Data Preprocessing Steps

### 1. Atmospheric Correction
- Percentile-based normalization (2-98th percentile)
- Removes atmospheric effects and reduces noise
- Applied per band

### 2. Normalization
- Min-Max scaling to [0, 1] range
- Ensures consistent value ranges across bands
- Improves model training stability

### 3. Stratified Train-Val-Test Split
- **Training Set**: 60% (16,200 images)
- **Validation Set**: 20% (5,400 images)
- **Test Set**: 20% (5,400 images)
- Stratified to maintain class distribution

## Generated Files

### Processed Data (in `processed_data/`)
```
X_train.npy          # Training images (12000, 12, 64, 64)
X_val.npy            # Validation images (4000, 12, 64, 64)
X_test.npy           # Test images (4000, 12, 64, 64)
y_train.npy          # Training labels (12000,)
y_val.npy            # Validation labels (4000,)
y_test.npy           # Test labels (4000,)
metadata.json        # Dataset metadata
vegetation_indices.csv  # Calculated NDVI, NDBI, NDWI statistics
```

### Visualizations (in `visualizations/`)
```
sample_images_rgb.png               # RGB composites of each land type
sample_images_false_color.png       # False color composites (NIR-R-G)
ndvi_maps.png                       # NDVI visualization
spectral_signatures.png             # Mean spectral curves per class
band_distributions.png              # Histogram analysis of bands
vegetation_indices_comparison.png   # Bar charts of mean indices
indices_heatmap.png                 # Heatmap of mean indices
data_split_distribution.png         # Class distribution in splits
```

### Reports
```
EDA_REPORT.txt       # Summary statistics and findings
```

## Usage Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Main Notebook
```bash
jupyter notebook 01_eda_and_preprocessing.ipynb
```

## Key Findings

### Dataset Characteristics
- **Balanced Distribution**: Well-distributed across classes (2,000-3,000 per class)
- **Spatial Resolution**: 64×64 pixels at 10m native resolution = ~640×640m ground coverage
- **Spectral Information**: Rich 12-band coverage including visible, NIR, and SWIR

### Spectral Distinctions
- **Forest**: High NDVI, distinctive vegetation signature
- **Water (River, SeaLake)**: Low NDVI, high water absorption in red/NIR
- **Urban (Residential, Industrial, Highway)**: High NDBI, low NDVI
- **Crops**: Moderate-high NDVI with temporal variability
- **Pasture**: Similar to crops but different texture patterns

### Data Quality
- No missing values across all bands
- Consistent image dimensions (64×64)
- Value ranges within expected Sentinel-2 specifications
- Proper class distribution maintained after splitting

## Next Steps (Milestone 2)
-Analyze the relationship between different spectral bands and land types 
  to determine which bands are most useful for classification.
-Visualize the correlation between the spectral bands and the land types.
- Use dimensionality reduction techniques.
- Choose suitable machine learning models for image classification.
- Implement transfer learning approaches
- Model training, validation, and testing
- Performance evaluation and optimization
- 

## References
- Helber et al. (2019). "EuroSAT: A Novel Dataset and Deep Learning Benchmark for Land Use and Land Cover Classification"
- Sentinel-2 User Handbook: https://sentinels.copernicus.eu/web/sentinel/user-guides/sentinel-2-msi
- NDVI, NDBI, NDWI Indices: Remote Sensing Fundamentals

## File Structure
```
milestone1/
├── 01_eda_and_preprocessing.ipynb    # Main EDA notebook
├── utils.py                          # Utility functions
├── requirements.txt                  # Python dependencies
├── README.md                         # This file
├── processed_data/                   # Output directory
│   ├── X_train.npy
│   ├── X_val.npy
│   ├── X_test.npy
│   ├── y_train.npy
│   ├── y_val.npy
│   ├── y_test.npy
│   ├── metadata.json
│   └── vegetation_indices.csv
├── visualizations/                   # Output directory
│   ├── sample_images_rgb.png
│   ├── sample_images_false_color.png
│   ├── ndvi_maps.png
│   ├── spectral_signatures.png
│   ├── band_distributions.png
│   ├── vegetation_indices_comparison.png
│   ├── indices_heatmap.png
│   └── data_split_distribution.png
└── EDA_REPORT.txt                    # Summary report
```

## Notes
- All images are normalized to 64×64 pixels for consistency
- Preprocessing is applied before model training
- Vegetation indices are computed as external features
- All data splits are stratified to maintain class balance
