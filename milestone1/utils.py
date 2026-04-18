"""
Utility functions for Land Type Classification using Sentinel-2 Satellite Images
"""

import numpy as np
import rasterio
from pathlib import Path
from typing import Tuple, Optional, List
import json


class SentinelConfig:
    """Configuration for Sentinel-2 data"""

    BANDS = {
        1: "Coastal aerosol (B1)",
        2: "Blue (B2)",
        3: "Green (B3)",
        4: "Red (B4)",
        5: "Vegetation Red Edge (B5)",
        6: "Vegetation Red Edge (B6)",
        7: "Vegetation Red Edge (B7)",
        8: "NIR (B8)",
        9: "Narrow NIR (B8A)",
        10: "Water Vapor (B9)",
        11: "SWIR (B11)",
        12: "SWIR (B12)"
    }

    LAND_TYPES = [
        "AnnualCrop",
        "Forest",
        "HerbaceousVegetation",
        "Highway",
        "Industrial",
        "Pasture",
        "PermanentCrop",
        "Residential",
        "River",
        "SeaLake"
    ]

    # Band indices (0-indexed)
    BAND_INDICES = {
        'coastal_aerosol': 0,  # B1
        'blue': 1,              # B2
        'green': 2,             # B3
        'red': 3,               # B4
        'rededge1': 4,          # B5
        'rededge2': 5,          # B6
        'rededge3': 6,          # B7
        'nir': 7,               # B8
        'rededge4': 8,          # B8A
        'water_vapor': 9,       # B9
        'swir1': 10,            # B11
        'swir2': 11             # B12
    }


class ImageLoader:
    """Load and process satellite images"""

    @staticmethod
    def load_tif_image(file_path: str) -> Tuple[np.ndarray, dict]:
        """Load a TIF image with all bands using rasterio"""
        with rasterio.open(file_path) as src:
            data = src.read()
            meta = src.meta
        return data, meta

    @staticmethod
    def load_dataset(base_path: Path, land_types: List[str],
                     limit: Optional[int] = None) -> Tuple[List, List]:
        """Load images from dataset"""
        all_images = []
        all_labels = []

        for label_idx, land_type in enumerate(land_types):
            land_dir = base_path / land_type
            image_files = sorted(land_dir.glob('*.tif'))

            if limit:
                image_files = image_files[:limit]

            for img_path in image_files:
                try:
                    data, _ = ImageLoader.load_tif_image(str(img_path))
                    all_images.append(data)
                    all_labels.append(label_idx)
                except Exception as e:
                    print(f"Error loading {img_path}: {e}")

        return all_images, all_labels


class ImageProcessor:
    """Process satellite images"""

    @staticmethod
    def normalize_band(band: np.ndarray, percentile_min: int = 2,
                       percentile_max: int = 98) -> np.ndarray:
        """Normalize band for visualization"""
        p_min = np.percentile(band, percentile_min)
        p_max = np.percentile(band, percentile_max)
        normalized = np.clip((band - p_min) / (p_max - p_min + 1e-5), 0, 1)
        return normalized

    @staticmethod
    def normalize_image(image_data: np.ndarray, method: str = 'minmax') -> np.ndarray:
        """
        Normalize image data
        Methods: 'minmax' for 0-1 scaling, 'standard' for standardization
        """
        if method == 'minmax':
            min_val = image_data.min()
            max_val = image_data.max()
            normalized = (image_data - min_val) / (max_val - min_val + 1e-5)
        elif method == 'standard':
            mean_val = image_data.mean()
            std_val = image_data.std()
            normalized = (image_data - mean_val) / (std_val + 1e-5)
        else:
            raise ValueError(f"Unknown normalization method: {method}")

        return normalized

    @staticmethod
    def apply_atmospheric_correction(image_data: np.ndarray) -> np.ndarray:
        """Simple atmospheric correction using percentile normalization"""
        corrected = np.zeros_like(image_data, dtype=np.float32)
        for band_idx in range(image_data.shape[0]):
            p2 = np.percentile(image_data[band_idx], 2)
            p98 = np.percentile(image_data[band_idx], 98)
            corrected[band_idx] = np.clip((image_data[band_idx] - p2) / (p98 - p2), 0, 1)
        return corrected

    @staticmethod
    def preprocess_image(image_data: np.ndarray,
                        atmospheric_correct: bool = True,
                        normalize: bool = True) -> np.ndarray:
        """Complete preprocessing pipeline"""
        if atmospheric_correct:
            image_data = ImageProcessor.apply_atmospheric_correction(image_data)
        if normalize:
            image_data = ImageProcessor.normalize_image(image_data, method='minmax')
        return image_data


class VegetationIndices:
    """Calculate vegetation indices"""

    @staticmethod
    def calculate_ndvi(image_data: np.ndarray) -> np.ndarray:
        """
        Calculate Normalized Difference Vegetation Index (NDVI)
        NDVI = (NIR - Red) / (NIR + Red)
        Band 8 is NIR, Band 4 is Red
        """
        nir = image_data[SentinelConfig.BAND_INDICES['nir']].astype(float)
        red = image_data[SentinelConfig.BAND_INDICES['red']].astype(float)
        ndvi = (nir - red) / (nir + red + 1e-5)
        return ndvi

    @staticmethod
    def calculate_ndbi(image_data: np.ndarray) -> np.ndarray:
        """
        Calculate Normalized Difference Built-up Index (NDBI)
        NDBI = (SWIR - NIR) / (SWIR + NIR)
        Band 11 is SWIR, Band 8 is NIR
        """
        swir = image_data[SentinelConfig.BAND_INDICES['swir1']].astype(float)
        nir = image_data[SentinelConfig.BAND_INDICES['nir']].astype(float)
        ndbi = (swir - nir) / (swir + nir + 1e-5)
        return ndbi

    @staticmethod
    def calculate_ndwi(image_data: np.ndarray) -> np.ndarray:
        """
        Calculate Normalized Difference Water Index (NDWI)
        NDWI = (NIR - SWIR) / (NIR + SWIR)
        Band 8 is NIR, Band 11 is SWIR
        """
        nir = image_data[SentinelConfig.BAND_INDICES['nir']].astype(float)
        swir = image_data[SentinelConfig.BAND_INDICES['swir1']].astype(float)
        ndwi = (nir - swir) / (nir + swir + 1e-5)
        return ndwi

    @staticmethod
    def calculate_all_indices(image_data: np.ndarray) -> dict:
        """Calculate all indices and return as dictionary"""
        return {
            'ndvi': VegetationIndices.calculate_ndvi(image_data),
            'ndbi': VegetationIndices.calculate_ndbi(image_data),
            'ndwi': VegetationIndices.calculate_ndwi(image_data)
        }


class CompositeCreator:
    """Create different band composites"""

    @staticmethod
    def create_rgb_composite(image_data: np.ndarray, r_band: int = 3,
                            g_band: int = 2, b_band: int = 1) -> np.ndarray:
        """Create RGB composite from specified bands (1-indexed)"""
        rgb = np.stack([
            ImageProcessor.normalize_band(image_data[r_band-1]),
            ImageProcessor.normalize_band(image_data[g_band-1]),
            ImageProcessor.normalize_band(image_data[b_band-1])
        ], axis=-1)
        return rgb

    @staticmethod
    def create_false_color_composite(image_data: np.ndarray, r_band: int = 8,
                                    g_band: int = 4, b_band: int = 3) -> np.ndarray:
        """Create False Color composite (NIR-Red-Green)"""
        return CompositeCreator.create_rgb_composite(image_data, r_band, g_band, b_band)

    @staticmethod
    def create_swir_composite(image_data: np.ndarray) -> np.ndarray:
        """Create SWIR composite (SWIR-NIR-Red)"""
        return CompositeCreator.create_rgb_composite(image_data, r_band=11,
                                                     g_band=8, b_band=4)


class MetadataManager:
    """Manage dataset metadata"""

    @staticmethod
    def create_metadata(image_shape: Tuple[int, ...], num_classes: int,
                       train_size: int, val_size: int, test_size: int) -> dict:
        """Create metadata dictionary"""
        return {
            'land_types': SentinelConfig.LAND_TYPES,
            'sentinel2_bands': SentinelConfig.BANDS,
            'image_shape': image_shape,
            'num_classes': num_classes,
            'train_size': train_size,
            'val_size': val_size,
            'test_size': test_size
        }

    @staticmethod
    def save_metadata(metadata: dict, output_path: Path):
        """Save metadata to JSON file"""
        with open(output_path, 'w') as f:
            json.dump(metadata, f, indent=2)

    @staticmethod
    def load_metadata(metadata_path: Path) -> dict:
        """Load metadata from JSON file"""
        with open(metadata_path, 'r') as f:
            return json.load(f)
