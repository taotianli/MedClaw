# Medical Data Analysis Guide

This guide covers common medical data analysis workflows using MedClaw.

## Table of Contents

1. [DICOM Image Analysis](#dicom-image-analysis)
2. [NIfTI Brain Imaging](#nifti-brain-imaging)
3. [Genomic Variant Analysis](#genomic-variant-analysis)
4. [Image Segmentation](#image-segmentation)
5. [Clinical Data Processing](#clinical-data-processing)

## DICOM Image Analysis

### Reading DICOM Files

```python
import pydicom
from container.medical-tools.dicom_utils import *

# Read single DICOM file
ds = pydicom.dcmread('scan.dcm')

# Extract metadata
metadata = extract_dicom_metadata(ds)
print(f"Patient: {metadata['patient_name']}")
print(f"Modality: {metadata['modality']}")
print(f"Study Date: {metadata['study_date']}")

# Access pixel data
pixel_array = ds.pixel_array
print(f"Image shape: {pixel_array.shape}")
```

### Processing DICOM Series

```python
# Read entire series from directory
series = read_dicom_series('/path/to/dicom/directory')
print(f"Found {len(series)} slices")

# Create 3D volume
volume, vol_metadata = create_volume_from_series(series)
print(f"Volume shape: {volume.shape}")
print(f"Spacing: {vol_metadata['spacing']}")
```

### CT Scan Analysis (Hounsfield Units)

```python
# Convert to Hounsfield Units
hu_array = get_hounsfield_units(ds)

# Analyze tissue types
bone_mask = hu_array > 300  # Bone
soft_tissue_mask = (hu_array > -100) & (hu_array < 100)  # Soft tissue
lung_mask = (hu_array > -1000) & (hu_array < -400)  # Lung
```

### Anonymization

```python
# Remove patient identifying information
anonymized_ds = anonymize_dicom(ds)
anonymized_ds.save_as('anonymized_scan.dcm')
```

## NIfTI Brain Imaging

### Loading and Analyzing NIfTI Files

```python
import nibabel as nib
from container.medical-tools.nifti_utils import *

# Load NIfTI file
data, img = load_nifti('brain.nii.gz')

# Get metadata
metadata = get_nifti_metadata(img)
print(f"Shape: {metadata['shape']}")
print(f"Voxel dimensions: {metadata['voxel_dimensions']}")

# Calculate statistics
stats = calculate_intensity_statistics(data)
print(f"Mean intensity: {stats['mean']}")
print(f"Std deviation: {stats['std']}")
```

### Brain Volume Calculation

```python
# Calculate brain volume
voxel_dims = img.header.get_zooms()[:3]
volume_info = calculate_brain_volume(data, voxel_dims, threshold=100)

print(f"Brain volume: {volume_info['total_volume_cm3']:.2f} cm³")
```

### Extracting Slices

```python
# Extract axial slice
axial_slice = extract_slice(data, axis=2, slice_idx=100)

# Extract coronal slice
coronal_slice = extract_slice(data, axis=1, slice_idx=128)

# Extract sagittal slice
sagittal_slice = extract_slice(data, axis=0, slice_idx=128)
```

### ROI Analysis

```python
# Create ROI mask
roi_mask = create_roi_mask(data, lower_threshold=100, upper_threshold=500)

# Calculate statistics within ROI
roi_stats = calculate_intensity_statistics(data, mask=roi_mask)
print(f"ROI mean: {roi_stats['mean']}")

# Calculate center of mass
com = get_center_of_mass(data, voxel_dims)
print(f"Center of mass: {com['physical_coordinates_mm']}")
```

## Genomic Variant Analysis

### VCF File Processing

```python
from container.medical-tools.genomics_utils import *

# Parse VCF file
variants = parse_vcf_file('variants.vcf', quality_threshold=30.0)
print(f"Found {len(variants)} high-quality variants")

# Get summary statistics
summary = get_variant_summary(variants)
print(f"Total variants: {summary['total_variants']}")
print(f"SNVs: {summary['by_type']['SNV']}")
print(f"Insertions: {summary['by_type']['INS']}")
print(f"Deletions: {summary['by_type']['DEL']}")

# Filter by region
chr1_variants = filter_variants_by_region(
    variants,
    chromosome='chr1',
    start=1000000,
    end=2000000
)
print(f"Variants in region: {len(chr1_variants)}")
```

### BAM File Analysis

```python
# Get BAM statistics
stats = get_bam_statistics('aligned.bam')
print(f"Total reads: {stats['total_reads']}")
print(f"Mapped reads: {stats['mapped_reads']}")
print(f"Mapping rate: {stats['mapping_rate']:.2f}%")

# Get coverage at specific position
coverage = get_coverage_at_position(
    'aligned.bam',
    chromosome='chr1',
    position=12345,
    window=50
)

for pos_info in coverage['coverage']:
    print(f"Position {pos_info['position']}: depth {pos_info['depth']}")
```

### FASTA Sequence Analysis

```python
# Parse FASTA file
sequences = parse_fasta_file('genome.fasta')

for seq in sequences:
    print(f"ID: {seq['id']}")
    print(f"Length: {seq['sequence_length']}")
    print(f"GC content: {seq['gc_content']:.2f}%")
```

## Image Segmentation

### Threshold Segmentation

```python
import SimpleITK as sitk
from container.medical-tools.segmentation_utils import *

# Load image
image = load_image('ct_scan.nii.gz')

# Threshold segmentation
segmentation = threshold_segmentation(image, lower=100, upper=400)

# Calculate volume
volume_info = calculate_volume_from_segmentation(segmentation)
print(f"Segmented volume: {volume_info['total_volume_cm3']:.2f} cm³")

# Save result
save_segmentation(segmentation, 'segmented.nii.gz')
```

### Automatic Segmentation

```python
# Otsu automatic thresholding
auto_seg = otsu_segmentation(image)

# Connected components analysis
labeled, stats = connected_components_analysis(auto_seg)
print(f"Found {stats['num_components']} components")

# Extract largest component
largest = extract_largest_component(auto_seg)
```

### Region Growing

```python
# Define seed points (x, y, z coordinates)
seed_points = [(128, 128, 64), (130, 130, 65)]

# Perform region growing
region_seg = region_growing_segmentation(
    image,
    seed_points=seed_points,
    lower=100,
    upper=300
)
```

### Morphological Operations

```python
# Dilate segmentation
dilated = morphological_operations(segmentation, 'dilate', radius=2)

# Erode segmentation
eroded = morphological_operations(segmentation, 'erode', radius=1)

# Smooth segmentation
smoothed = smooth_segmentation(segmentation, iterations=5)
```

### Segmentation Comparison

```python
# Calculate Dice coefficient between two segmentations
dice = calculate_dice_coefficient(segmentation1, segmentation2)
print(f"Dice coefficient: {dice:.3f}")
```

## Clinical Data Processing

### FHIR Patient Resources

```python
from container.medical-tools.clinical_utils import *

# Create patient resource
patient_data = {
    "id": "patient-001",
    "family_name": "Doe",
    "given_names": ["John"],
    "gender": "male",
    "birth_date": "1980-01-01"
}

patient = create_patient_resource(patient_data)
print(patient.json(indent=2))

# Anonymize patient data
anon_patient = anonymize_fhir_patient(patient)
```

### FHIR Observations

```python
# Create observation (e.g., vital sign)
observation_data = {
    "id": "obs-001",
    "status": "final",
    "code": "8867-4",  # LOINC code for heart rate
    "code_display": "Heart rate",
    "patient_reference": "Patient/patient-001",
    "value_quantity": {
        "value": 72,
        "unit": "beats/minute",
        "system": "http://unitsofmeasure.org",
        "code": "/min"
    }
}

observation = create_observation_resource(observation_data)

# Parse observation
obs_info = parse_observation_resource(observation.json())
print(f"Code: {obs_info['code']['display']}")
print(f"Value: {obs_info['value']['value']} {obs_info['value']['unit']}")
```

### Extracting Vital Signs

```python
# Extract vital signs from observations
observations = [obs1, obs2, obs3]  # List of Observation resources
vital_signs = extract_vital_signs(observations)

print(f"Heart rate: {vital_signs['heart_rate']}")
print(f"Blood pressure: {vital_signs['blood_pressure_systolic']}/{vital_signs['blood_pressure_diastolic']}")
print(f"Temperature: {vital_signs['temperature']}")
```

### FHIR Validation

```python
# Validate FHIR resource
result = validate_fhir_resource(patient_json, "Patient")
if result['valid']:
    print("Valid FHIR resource")
else:
    print(f"Validation error: {result['error']}")
```

## Common Workflows

### Complete CT Analysis Pipeline

```python
# 1. Load DICOM series
series = read_dicom_series('/data/ct_study')

# 2. Create 3D volume
volume, metadata = create_volume_from_series(series)

# 3. Convert to Hounsfield Units
hu_volume = np.zeros_like(volume)
for i, ds in enumerate(series):
    hu_volume[i] = get_hounsfield_units(ds)

# 4. Segment organ (e.g., liver)
# Convert to SimpleITK image
sitk_image = sitk.GetImageFromArray(hu_volume)
sitk_image.SetSpacing(metadata['spacing'])

# Threshold for liver (typically 40-60 HU)
liver_seg = threshold_segmentation(sitk_image, 40, 60)

# 5. Calculate liver volume
liver_volume = calculate_volume_from_segmentation(liver_seg)
print(f"Liver volume: {liver_volume['total_volume_cm3']:.2f} cm³")

# 6. Save results
save_segmentation(liver_seg, 'liver_segmentation.nii.gz')
```

### Genomic Variant Annotation Pipeline

```python
# 1. Parse VCF file
variants = parse_vcf_file('sample.vcf', quality_threshold=30)

# 2. Get summary
summary = get_variant_summary(variants)

# 3. Filter high-quality variants
high_qual_variants = [v for v in variants if v['quality'] and v['quality'] > 50]

# 4. Annotate variant types
for variant in high_qual_variants:
    if variant['alternate']:
        var_type = annotate_variant_type(
            variant['reference'],
            variant['alternate'][0]
        )
        variant['type'] = var_type

# 5. Filter by genomic region of interest
roi_variants = filter_variants_by_region(
    high_qual_variants,
    chromosome='chr17',
    start=7571720,  # TP53 gene region
    end=7590868
)

print(f"Found {len(roi_variants)} variants in TP53 region")
```

## Best Practices

### Data Security
- Always anonymize patient data before analysis
- Use encrypted storage for sensitive medical data
- Implement proper access controls
- Maintain audit logs of data access

### Performance Optimization
- Use memory-mapped files for large datasets
- Process data in chunks when possible
- Leverage GPU acceleration for deep learning tasks
- Cache intermediate results

### Quality Control
- Validate input data formats
- Check for missing or corrupted data
- Verify image orientation and spacing
- Document all processing steps

### Reproducibility
- Record all parameters and thresholds used
- Save processing scripts with results
- Version control analysis code
- Document software versions and dependencies
