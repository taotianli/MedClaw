# Medical Tools Configuration

This directory contains configurations and utilities for medical data analysis.

## Installed Tools

### Medical Imaging
- **pydicom** - DICOM file reading and manipulation
- **nibabel** - Neuroimaging data I/O (NIfTI, Analyze, etc.)
- **SimpleITK** - Image analysis, segmentation, and registration
- **scikit-image** - Image processing algorithms
- **opencv-python** - Computer vision and image processing
- **Pillow** - Image file format support

### Genomics
- **BioPython** - Sequence analysis and bioinformatics
- **pysam** - SAM/BAM/CRAM file manipulation
- **PyVCF3** - VCF file parsing and manipulation
- **scikit-bio** - Bioinformatics data structures and algorithms

### Clinical Data
- **fhir.resources** - FHIR resource handling
- **hl7apy** - HL7 v2 message parsing and generation

### Data Analysis
- **numpy** - Numerical computing
- **scipy** - Scientific computing
- **pandas** - Data manipulation and analysis
- **matplotlib** - Data visualization

## Usage Examples

### DICOM Processing
```python
import pydicom
import numpy as np

# Read DICOM file
ds = pydicom.dcmread('scan.dcm')
print(f"Patient: {ds.PatientName}")
print(f"Modality: {ds.Modality}")

# Access pixel data
pixel_array = ds.pixel_array
print(f"Image shape: {pixel_array.shape}")
```

### NIfTI Analysis
```python
import nibabel as nib
import numpy as np

# Load NIfTI file
img = nib.load('brain.nii.gz')
data = img.get_fdata()
print(f"Volume shape: {data.shape}")
print(f"Voxel dimensions: {img.header.get_zooms()}")
```

### VCF Processing
```python
import vcf

# Read VCF file
vcf_reader = vcf.Reader(open('variants.vcf', 'r'))

for record in vcf_reader:
    print(f"Variant: {record.CHROM}:{record.POS} {record.REF}>{record.ALT}")
    print(f"Quality: {record.QUAL}")
```

### BAM File Analysis
```python
import pysam

# Open BAM file
bamfile = pysam.AlignmentFile("aligned.bam", "rb")

# Count reads
total_reads = bamfile.count()
print(f"Total reads: {total_reads}")

# Iterate over reads
for read in bamfile.fetch():
    print(f"Read: {read.query_name}, Position: {read.reference_start}")
```

### Image Segmentation
```python
import SimpleITK as sitk
import numpy as np

# Read medical image
image = sitk.ReadImage('ct_scan.nii.gz')

# Apply threshold segmentation
threshold_filter = sitk.BinaryThresholdImageFilter()
threshold_filter.SetLowerThreshold(100)
threshold_filter.SetUpperThreshold(400)
segmented = threshold_filter.Execute(image)

# Save result
sitk.WriteImage(segmented, 'segmented.nii.gz')
```

## Adding More Tools

To add additional medical analysis tools, update the Dockerfile:

```dockerfile
RUN /opt/medclaw-env/bin/pip install --no-cache-dir \
    your-package-name==version
```

Common additions:
- **MONAI** - Medical imaging AI toolkit
- **nilearn** - Neuroimaging machine learning
- **openslide-python** - Whole slide imaging
- **pyradiomics** - Radiomics feature extraction
- **deepvariant** - Genomic variant calling
