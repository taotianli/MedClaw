#!/usr/bin/env python3
"""
DICOM Analysis Utilities for MedClaw
Provides helper functions for DICOM file processing and analysis
"""

import pydicom
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import json


def read_dicom_series(directory: str) -> List[pydicom.Dataset]:
    """
    Read all DICOM files from a directory and sort by instance number.

    Args:
        directory: Path to directory containing DICOM files

    Returns:
        List of sorted DICOM datasets
    """
    dicom_files = []
    path = Path(directory)

    for file_path in path.glob("*.dcm"):
        try:
            ds = pydicom.dcmread(str(file_path))
            dicom_files.append(ds)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")

    # Sort by instance number if available
    dicom_files.sort(key=lambda x: int(x.InstanceNumber) if hasattr(x, 'InstanceNumber') else 0)
    return dicom_files


def extract_dicom_metadata(ds: pydicom.Dataset) -> Dict:
    """
    Extract key metadata from a DICOM dataset.

    Args:
        ds: DICOM dataset

    Returns:
        Dictionary of metadata
    """
    metadata = {
        'patient_name': str(ds.PatientName) if hasattr(ds, 'PatientName') else 'Unknown',
        'patient_id': str(ds.PatientID) if hasattr(ds, 'PatientID') else 'Unknown',
        'study_date': str(ds.StudyDate) if hasattr(ds, 'StudyDate') else 'Unknown',
        'modality': str(ds.Modality) if hasattr(ds, 'Modality') else 'Unknown',
        'study_description': str(ds.StudyDescription) if hasattr(ds, 'StudyDescription') else '',
        'series_description': str(ds.SeriesDescription) if hasattr(ds, 'SeriesDescription') else '',
        'image_shape': ds.pixel_array.shape if hasattr(ds, 'pixel_array') else None,
        'pixel_spacing': list(ds.PixelSpacing) if hasattr(ds, 'PixelSpacing') else None,
        'slice_thickness': float(ds.SliceThickness) if hasattr(ds, 'SliceThickness') else None,
    }
    return metadata


def get_hounsfield_units(ds: pydicom.Dataset) -> Optional[np.ndarray]:
    """
    Convert DICOM pixel data to Hounsfield Units (for CT scans).

    Args:
        ds: DICOM dataset

    Returns:
        Numpy array in Hounsfield Units or None
    """
    if not hasattr(ds, 'pixel_array'):
        return None

    pixel_array = ds.pixel_array.astype(np.float64)

    # Apply rescale slope and intercept
    intercept = ds.RescaleIntercept if hasattr(ds, 'RescaleIntercept') else 0
    slope = ds.RescaleSlope if hasattr(ds, 'RescaleSlope') else 1

    hu_array = pixel_array * slope + intercept
    return hu_array


def create_volume_from_series(dicom_series: List[pydicom.Dataset]) -> Tuple[np.ndarray, Dict]:
    """
    Create a 3D volume from a series of DICOM slices.

    Args:
        dicom_series: List of DICOM datasets (sorted)

    Returns:
        Tuple of (3D numpy array, metadata dict)
    """
    if not dicom_series:
        raise ValueError("Empty DICOM series")

    # Get dimensions from first slice
    first_slice = dicom_series[0]
    img_shape = first_slice.pixel_array.shape

    # Create 3D array
    volume = np.zeros((len(dicom_series), img_shape[0], img_shape[1]))

    for i, ds in enumerate(dicom_series):
        volume[i, :, :] = ds.pixel_array

    # Extract spacing information
    metadata = {
        'spacing': [
            float(first_slice.SliceThickness) if hasattr(first_slice, 'SliceThickness') else 1.0,
            float(first_slice.PixelSpacing[0]) if hasattr(first_slice, 'PixelSpacing') else 1.0,
            float(first_slice.PixelSpacing[1]) if hasattr(first_slice, 'PixelSpacing') else 1.0,
        ],
        'shape': volume.shape,
        'modality': str(first_slice.Modality) if hasattr(first_slice, 'Modality') else 'Unknown'
    }

    return volume, metadata


def anonymize_dicom(ds: pydicom.Dataset) -> pydicom.Dataset:
    """
    Remove patient identifying information from DICOM dataset.

    Args:
        ds: DICOM dataset

    Returns:
        Anonymized DICOM dataset
    """
    # Tags to remove for anonymization
    tags_to_anonymize = [
        'PatientName',
        'PatientID',
        'PatientBirthDate',
        'PatientSex',
        'PatientAge',
        'PatientAddress',
        'InstitutionName',
        'InstitutionAddress',
        'ReferringPhysicianName',
        'PerformingPhysicianName',
        'OperatorsName',
    ]

    for tag in tags_to_anonymize:
        if hasattr(ds, tag):
            delattr(ds, tag)

    # Set anonymous patient ID
    ds.PatientName = "ANONYMOUS"
    ds.PatientID = "ANON"

    return ds


def calculate_statistics(pixel_array: np.ndarray) -> Dict:
    """
    Calculate basic statistics for image data.

    Args:
        pixel_array: Numpy array of pixel data

    Returns:
        Dictionary of statistics
    """
    return {
        'mean': float(np.mean(pixel_array)),
        'std': float(np.std(pixel_array)),
        'min': float(np.min(pixel_array)),
        'max': float(np.max(pixel_array)),
        'median': float(np.median(pixel_array)),
        'percentile_25': float(np.percentile(pixel_array, 25)),
        'percentile_75': float(np.percentile(pixel_array, 75)),
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python dicom_utils.py <dicom_file_or_directory>")
        sys.exit(1)

    path = Path(sys.argv[1])

    if path.is_file():
        # Single DICOM file
        ds = pydicom.dcmread(str(path))
        metadata = extract_dicom_metadata(ds)
        print(json.dumps(metadata, indent=2))

        if hasattr(ds, 'pixel_array'):
            stats = calculate_statistics(ds.pixel_array)
            print("\nImage Statistics:")
            print(json.dumps(stats, indent=2))

    elif path.is_dir():
        # DICOM series
        series = read_dicom_series(str(path))
        print(f"Found {len(series)} DICOM files")

        if series:
            metadata = extract_dicom_metadata(series[0])
            print("\nSeries Metadata:")
            print(json.dumps(metadata, indent=2))

            try:
                volume, vol_metadata = create_volume_from_series(series)
                print("\nVolume Information:")
                print(json.dumps(vol_metadata, indent=2))
            except Exception as e:
                print(f"Error creating volume: {e}")
