#!/usr/bin/env python3
"""
Image Segmentation Utilities for MedClaw
Provides helper functions for medical image segmentation
"""

import SimpleITK as sitk
import numpy as np
from pathlib import Path
from typing import Dict, Tuple, Optional, List
import json


def load_image(file_path: str) -> sitk.Image:
    """
    Load medical image using SimpleITK.

    Args:
        file_path: Path to image file

    Returns:
        SimpleITK image object
    """
    return sitk.ReadImage(file_path)


def threshold_segmentation(image: sitk.Image, lower: float, upper: float) -> sitk.Image:
    """
    Perform binary threshold segmentation.

    Args:
        image: Input SimpleITK image
        lower: Lower threshold value
        upper: Upper threshold value

    Returns:
        Binary segmented image
    """
    threshold_filter = sitk.BinaryThresholdImageFilter()
    threshold_filter.SetLowerThreshold(lower)
    threshold_filter.SetUpperThreshold(upper)
    threshold_filter.SetInsideValue(1)
    threshold_filter.SetOutsideValue(0)

    return threshold_filter.Execute(image)


def otsu_segmentation(image: sitk.Image) -> sitk.Image:
    """
    Perform Otsu automatic threshold segmentation.

    Args:
        image: Input SimpleITK image

    Returns:
        Binary segmented image
    """
    otsu_filter = sitk.OtsuThresholdImageFilter()
    otsu_filter.SetInsideValue(0)
    otsu_filter.SetOutsideValue(1)

    return otsu_filter.Execute(image)


def region_growing_segmentation(image: sitk.Image, seed_points: List[Tuple[int, int, int]],
                                lower: float, upper: float) -> sitk.Image:
    """
    Perform connected threshold region growing segmentation.

    Args:
        image: Input SimpleITK image
        seed_points: List of seed point coordinates [(x, y, z), ...]
        lower: Lower threshold
        upper: Upper threshold

    Returns:
        Segmented image
    """
    seg_filter = sitk.ConnectedThresholdImageFilter()
    seg_filter.SetLower(lower)
    seg_filter.SetUpper(upper)
    seg_filter.SetSeedList(seed_points)
    seg_filter.SetReplaceValue(1)

    return seg_filter.Execute(image)


def watershed_segmentation(image: sitk.Image, level: float = 0.5) -> sitk.Image:
    """
    Perform watershed segmentation.

    Args:
        image: Input SimpleITK image
        level: Water level parameter

    Returns:
        Segmented image with labeled regions
    """
    # Apply gradient magnitude
    gradient = sitk.GradientMagnitude(image)

    # Watershed segmentation
    watershed = sitk.MorphologicalWatershed(gradient, level=level)

    return watershed


def morphological_operations(image: sitk.Image, operation: str, radius: int = 1) -> sitk.Image:
    """
    Apply morphological operations to binary image.

    Args:
        image: Binary SimpleITK image
        operation: Operation type ('dilate', 'erode', 'open', 'close')
        radius: Structuring element radius

    Returns:
        Processed image
    """
    if operation == 'dilate':
        return sitk.BinaryDilate(image, [radius] * image.GetDimension())
    elif operation == 'erode':
        return sitk.BinaryErode(image, [radius] * image.GetDimension())
    elif operation == 'open':
        return sitk.BinaryMorphologicalOpening(image, [radius] * image.GetDimension())
    elif operation == 'close':
        return sitk.BinaryMorphologicalClosing(image, [radius] * image.GetDimension())
    else:
        raise ValueError(f"Unknown operation: {operation}")


def connected_components_analysis(binary_image: sitk.Image) -> Tuple[sitk.Image, Dict]:
    """
    Perform connected components analysis.

    Args:
        binary_image: Binary SimpleITK image

    Returns:
        Tuple of (labeled image, statistics dict)
    """
    # Label connected components
    labeled = sitk.ConnectedComponent(binary_image)

    # Calculate statistics
    stats_filter = sitk.LabelShapeStatisticsImageFilter()
    stats_filter.Execute(labeled)

    labels = stats_filter.GetLabels()

    statistics = {
        'num_components': len(labels),
        'components': []
    }

    for label in labels:
        component_stats = {
            'label': int(label),
            'num_pixels': int(stats_filter.GetNumberOfPixels(label)),
            'physical_size': float(stats_filter.GetPhysicalSize(label)),
            'centroid': [float(x) for x in stats_filter.GetCentroid(label)],
            'bounding_box': [int(x) for x in stats_filter.GetBoundingBox(label)]
        }
        statistics['components'].append(component_stats)

    return labeled, statistics


def calculate_dice_coefficient(segmentation1: sitk.Image, segmentation2: sitk.Image) -> float:
    """
    Calculate Dice similarity coefficient between two segmentations.

    Args:
        segmentation1: First binary segmentation
        segmentation2: Second binary segmentation

    Returns:
        Dice coefficient (0-1)
    """
    overlap_filter = sitk.LabelOverlapMeasuresImageFilter()
    overlap_filter.Execute(segmentation1, segmentation2)

    return overlap_filter.GetDiceCoefficient()


def extract_largest_component(binary_image: sitk.Image) -> sitk.Image:
    """
    Extract the largest connected component from binary image.

    Args:
        binary_image: Binary SimpleITK image

    Returns:
        Binary image with only largest component
    """
    labeled, stats = connected_components_analysis(binary_image)

    if stats['num_components'] == 0:
        return binary_image

    # Find largest component
    largest = max(stats['components'], key=lambda x: x['num_pixels'])
    largest_label = largest['label']

    # Create binary mask of largest component
    return sitk.BinaryThreshold(labeled, largest_label, largest_label, 1, 0)


def smooth_segmentation(binary_image: sitk.Image, iterations: int = 5) -> sitk.Image:
    """
    Smooth binary segmentation using morphological operations.

    Args:
        binary_image: Binary SimpleITK image
        iterations: Number of smoothing iterations

    Returns:
        Smoothed binary image
    """
    # Apply closing followed by opening
    smoothed = binary_image

    for _ in range(iterations):
        smoothed = sitk.BinaryMorphologicalClosing(smoothed, [1] * smoothed.GetDimension())
        smoothed = sitk.BinaryMorphologicalOpening(smoothed, [1] * smoothed.GetDimension())

    return smoothed


def calculate_volume_from_segmentation(segmentation: sitk.Image) -> Dict:
    """
    Calculate volume from binary segmentation.

    Args:
        segmentation: Binary SimpleITK image

    Returns:
        Dictionary with volume information
    """
    # Get spacing
    spacing = segmentation.GetSpacing()
    voxel_volume = spacing[0] * spacing[1] * spacing[2]

    # Count foreground voxels
    stats = sitk.LabelStatisticsImageFilter()
    stats.Execute(segmentation, segmentation)

    num_voxels = stats.GetCount(1)

    volume_mm3 = num_voxels * voxel_volume
    volume_cm3 = volume_mm3 / 1000

    return {
        'num_voxels': int(num_voxels),
        'voxel_volume_mm3': float(voxel_volume),
        'total_volume_mm3': float(volume_mm3),
        'total_volume_cm3': float(volume_cm3)
    }


def save_segmentation(image: sitk.Image, output_path: str):
    """
    Save segmentation to file.

    Args:
        image: SimpleITK image
        output_path: Output file path
    """
    sitk.WriteImage(image, output_path)
    print(f"Saved segmentation to: {output_path}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python segmentation_utils.py <image_file> [lower_threshold] [upper_threshold]")
        sys.exit(1)

    file_path = sys.argv[1]

    if not Path(file_path).exists():
        print(f"File not found: {file_path}")
        sys.exit(1)

    print(f"Loading image: {file_path}")
    image = load_image(file_path)

    # Perform threshold segmentation
    if len(sys.argv) >= 4:
        lower = float(sys.argv[2])
        upper = float(sys.argv[3])
        print(f"\nPerforming threshold segmentation ({lower} - {upper})...")
        segmentation = threshold_segmentation(image, lower, upper)
    else:
        print("\nPerforming Otsu segmentation...")
        segmentation = otsu_segmentation(image)

    # Calculate volume
    volume_info = calculate_volume_from_segmentation(segmentation)
    print("\nSegmentation Volume:")
    print(json.dumps(volume_info, indent=2))

    # Connected components analysis
    labeled, stats = connected_components_analysis(segmentation)
    print(f"\nFound {stats['num_components']} connected components")

    if stats['num_components'] > 0:
        print("\nLargest components:")
        sorted_components = sorted(stats['components'], key=lambda x: x['num_pixels'], reverse=True)
        for comp in sorted_components[:5]:
            print(f"  Label {comp['label']}: {comp['num_pixels']} pixels, {comp['physical_size']:.2f} mm³")
