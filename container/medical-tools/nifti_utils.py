#!/usr/bin/env python3
"""
NIfTI Analysis Utilities for MedClaw
Provides helper functions for neuroimaging data processing
"""

import nibabel as nib
import numpy as np
from pathlib import Path
from typing import Dict, Tuple, Optional
import json


def load_nifti(file_path: str) -> Tuple[np.ndarray, nib.Nifti1Image]:
    """
    Load NIfTI file and return data array and image object.

    Args:
        file_path: Path to NIfTI file

    Returns:
        Tuple of (data array, NIfTI image object)
    """
    img = nib.load(file_path)
    data = img.get_fdata()
    return data, img


def get_nifti_metadata(img: nib.Nifti1Image) -> Dict:
    """
    Extract metadata from NIfTI image.

    Args:
        img: NIfTI image object

    Returns:
        Dictionary of metadata
    """
    header = img.header

    metadata = {
        'shape': list(img.shape),
        'voxel_dimensions': list(header.get_zooms()),
        'data_type': str(header.get_data_dtype()),
        'affine_matrix': img.affine.tolist(),
        'qform_code': int(header['qform_code']),
        'sform_code': int(header['sform_code']),
        'units': {
            'spatial': header.get_xyzt_units()[0],
            'temporal': header.get_xyzt_units()[1]
        }
    }

    return metadata


def calculate_brain_volume(data: np.ndarray, voxel_dims: Tuple[float, float, float],
                          threshold: float = 0) -> Dict:
    """
    Calculate brain volume from segmented data.

    Args:
        data: 3D numpy array
        voxel_dims: Voxel dimensions (x, y, z) in mm
        threshold: Threshold for binary mask

    Returns:
        Dictionary with volume information
    """
    # Create binary mask
    mask = data > threshold

    # Count voxels
    voxel_count = np.sum(mask)

    # Calculate voxel volume in mm³
    voxel_volume = voxel_dims[0] * voxel_dims[1] * voxel_dims[2]

    # Total volume
    total_volume_mm3 = voxel_count * voxel_volume
    total_volume_cm3 = total_volume_mm3 / 1000

    return {
        'voxel_count': int(voxel_count),
        'voxel_volume_mm3': float(voxel_volume),
        'total_volume_mm3': float(total_volume_mm3),
        'total_volume_cm3': float(total_volume_cm3)
    }


def extract_slice(data: np.ndarray, axis: int, slice_idx: int) -> np.ndarray:
    """
    Extract a 2D slice from 3D volume.

    Args:
        data: 3D numpy array
        axis: Axis to slice (0=sagittal, 1=coronal, 2=axial)
        slice_idx: Slice index

    Returns:
        2D numpy array
    """
    if axis == 0:
        return data[slice_idx, :, :]
    elif axis == 1:
        return data[:, slice_idx, :]
    elif axis == 2:
        return data[:, :, slice_idx]
    else:
        raise ValueError("Axis must be 0, 1, or 2")


def calculate_intensity_statistics(data: np.ndarray, mask: Optional[np.ndarray] = None) -> Dict:
    """
    Calculate intensity statistics for volume data.

    Args:
        data: 3D numpy array
        mask: Optional binary mask to restrict analysis

    Returns:
        Dictionary of statistics
    """
    if mask is not None:
        masked_data = data[mask > 0]
    else:
        masked_data = data.flatten()

    # Remove NaN and infinite values
    masked_data = masked_data[np.isfinite(masked_data)]

    if len(masked_data) == 0:
        return {'error': 'No valid data points'}

    return {
        'mean': float(np.mean(masked_data)),
        'std': float(np.std(masked_data)),
        'min': float(np.min(masked_data)),
        'max': float(np.max(masked_data)),
        'median': float(np.median(masked_data)),
        'percentile_5': float(np.percentile(masked_data, 5)),
        'percentile_95': float(np.percentile(masked_data, 95)),
        'non_zero_voxels': int(np.sum(masked_data != 0))
    }


def resample_to_resolution(img: nib.Nifti1Image, target_resolution: Tuple[float, float, float]) -> nib.Nifti1Image:
    """
    Resample NIfTI image to target resolution.

    Args:
        img: NIfTI image object
        target_resolution: Target voxel dimensions (x, y, z) in mm

    Returns:
        Resampled NIfTI image
    """
    from scipy.ndimage import zoom

    # Get current resolution
    current_resolution = img.header.get_zooms()[:3]

    # Calculate zoom factors
    zoom_factors = [curr / target for curr, target in zip(current_resolution, target_resolution)]

    # Resample data
    data = img.get_fdata()
    resampled_data = zoom(data, zoom_factors, order=1)

    # Update affine matrix
    new_affine = img.affine.copy()
    new_affine[:3, :3] = new_affine[:3, :3] / np.array(zoom_factors)[:, np.newaxis]

    # Create new image
    resampled_img = nib.Nifti1Image(resampled_data, new_affine)

    return resampled_img


def create_roi_mask(data: np.ndarray, lower_threshold: float, upper_threshold: float) -> np.ndarray:
    """
    Create binary ROI mask based on intensity thresholds.

    Args:
        data: 3D numpy array
        lower_threshold: Lower intensity threshold
        upper_threshold: Upper intensity threshold

    Returns:
        Binary mask array
    """
    mask = np.logical_and(data >= lower_threshold, data <= upper_threshold)
    return mask.astype(np.uint8)


def get_center_of_mass(data: np.ndarray, voxel_dims: Tuple[float, float, float]) -> Dict:
    """
    Calculate center of mass for volume data.

    Args:
        data: 3D numpy array
        voxel_dims: Voxel dimensions (x, y, z) in mm

    Returns:
        Dictionary with center of mass coordinates
    """
    from scipy.ndimage import center_of_mass

    com_voxels = center_of_mass(data)

    # Convert to physical coordinates
    com_mm = [coord * dim for coord, dim in zip(com_voxels, voxel_dims)]

    return {
        'voxel_coordinates': [float(x) for x in com_voxels],
        'physical_coordinates_mm': [float(x) for x in com_mm]
    }


def save_nifti(data: np.ndarray, affine: np.ndarray, output_path: str):
    """
    Save numpy array as NIfTI file.

    Args:
        data: 3D numpy array
        affine: 4x4 affine transformation matrix
        output_path: Output file path
    """
    img = nib.Nifti1Image(data, affine)
    nib.save(img, output_path)
    print(f"Saved NIfTI file to: {output_path}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python nifti_utils.py <nifti_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not Path(file_path).exists():
        print(f"File not found: {file_path}")
        sys.exit(1)

    print(f"Loading NIfTI file: {file_path}")
    data, img = load_nifti(file_path)

    print("\nMetadata:")
    metadata = get_nifti_metadata(img)
    print(json.dumps(metadata, indent=2))

    print("\nIntensity Statistics:")
    stats = calculate_intensity_statistics(data)
    print(json.dumps(stats, indent=2))

    print("\nVolume Information:")
    voxel_dims = img.header.get_zooms()[:3]
    volume_info = calculate_brain_volume(data, voxel_dims, threshold=0)
    print(json.dumps(volume_info, indent=2))

    print("\nCenter of Mass:")
    com = get_center_of_mass(data, voxel_dims)
    print(json.dumps(com, indent=2))
