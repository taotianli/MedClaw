# Medical Data Formats Supported by MedClaw

This document describes the medical data formats that MedClaw can process and analyze.

## Medical Imaging Formats

### DICOM (Digital Imaging and Communications in Medicine)

**File Extensions:** `.dcm`, `.dicom`

**Description:** Industry standard for medical imaging data. Contains both image data and metadata (patient info, acquisition parameters, etc.).

**Modalities Supported:**
- CT (Computed Tomography)
- MRI (Magnetic Resonance Imaging)
- X-Ray
- Ultrasound
- PET (Positron Emission Tomography)
- Mammography
- Nuclear Medicine

**Key Features:**
- Patient demographics
- Study and series information
- Image acquisition parameters
- Pixel data with proper scaling
- Hounsfield Units for CT

**Example Usage:**
```python
import pydicom
ds = pydicom.dcmread('scan.dcm')
print(f"Modality: {ds.Modality}")
print(f"Patient: {ds.PatientName}")
pixel_array = ds.pixel_array
```

### NIfTI (Neuroimaging Informatics Technology Initiative)

**File Extensions:** `.nii`, `.nii.gz`

**Description:** Common format for neuroimaging data, especially fMRI and structural brain imaging.

**Key Features:**
- 3D/4D volume data
- Affine transformation matrix
- Voxel dimensions and spacing
- Data type specification
- Compressed format support (.gz)

**Example Usage:**
```python
import nibabel as nib
img = nib.load('brain.nii.gz')
data = img.get_fdata()
affine = img.affine
```

### NRRD (Nearly Raw Raster Data)

**File Extensions:** `.nrrd`, `.nhdr`

**Description:** Simple format for multi-dimensional raster data, commonly used in medical imaging research.

**Key Features:**
- N-dimensional arrays
- Flexible metadata
- Multiple encoding options
- Space directions and origins

### Analyze Format

**File Extensions:** `.hdr`, `.img`

**Description:** Legacy neuroimaging format, predecessor to NIfTI.

**Note:** Consider converting to NIfTI for better compatibility.

### TIFF/BigTIFF

**File Extensions:** `.tif`, `.tiff`

**Description:** Used for microscopy and whole slide imaging.

**Key Features:**
- Multi-page support
- Large file support (BigTIFF)
- Pyramidal structure for whole slide images
- Metadata in TIFF tags

### Whole Slide Imaging Formats

**File Extensions:** `.svs`, `.ndpi`, `.vsi`, `.scn`

**Description:** Proprietary formats for digital pathology.

**Supported Formats:**
- Aperio SVS (.svs)
- Hamamatsu NDPI (.ndpi)
- Olympus VSI (.vsi)
- Leica SCN (.scn)

**Note:** Requires OpenSlide library for reading.

## Genomic Data Formats

### FASTQ

**File Extensions:** `.fastq`, `.fq`, `.fastq.gz`, `.fq.gz`

**Description:** Text-based format for storing nucleotide sequences and quality scores.

**Structure:**
```
@SEQ_ID
GATTTGGGGTTCAAAGCAGTATCGATCAAATAGTAAATCCATTTGTTCAACTCACAGTTT
+
!''*((((***+))%%%++)(%%%%).1***-+*''))**55CCF>>>>>>CCCCCCC65
```

**Key Features:**
- Sequence identifier
- Raw sequence
- Quality scores (Phred scores)
- Compressed format support

### FASTA

**File Extensions:** `.fasta`, `.fa`, `.fna`, `.ffn`, `.faa`, `.frn`

**Description:** Text-based format for nucleotide or protein sequences.

**Structure:**
```
>seq1 description
ATCGATCGATCGATCG
>seq2 description
GCTAGCTAGCTAGCTA
```

**Variants:**
- `.fna` - nucleic acid
- `.faa` - amino acid
- `.ffn` - nucleotide coding regions
- `.frn` - non-coding RNA

### SAM/BAM/CRAM

**File Extensions:** `.sam`, `.bam`, `.cram`

**Description:** Sequence alignment formats.

**Formats:**
- **SAM** - Text format (human-readable)
- **BAM** - Binary compressed SAM
- **CRAM** - Reference-based compression

**Key Features:**
- Alignment information
- CIGAR strings
- Quality scores
- Flags for read properties
- Optional tags

**Example Usage:**
```python
import pysam
bamfile = pysam.AlignmentFile("aligned.bam", "rb")
for read in bamfile.fetch():
    print(read.query_name, read.reference_start)
```

### VCF/BCF (Variant Call Format)

**File Extensions:** `.vcf`, `.vcf.gz`, `.bcf`

**Description:** Format for storing gene sequence variations.

**Key Features:**
- Chromosome and position
- Reference and alternate alleles
- Quality scores
- Filter status
- INFO and FORMAT fields
- Genotype information

**Example Structure:**
```
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT  SAMPLE
chr1    12345   rs123   A       G       99      PASS    DP=100  GT:DP   0/1:50
```

### BED (Browser Extensible Data)

**File Extensions:** `.bed`

**Description:** Tab-delimited format for genomic regions.

**Structure:**
```
chr1    1000    2000    feature1    100     +
chr1    3000    4000    feature2    200     -
```

**Variants:**
- BED3 (minimal: chr, start, end)
- BED6 (adds name, score, strand)
- BED12 (full format with blocks)

### GFF/GTF (General Feature Format)

**File Extensions:** `.gff`, `.gff3`, `.gtf`

**Description:** Format for genomic annotations.

**Key Features:**
- Gene structures
- Transcript annotations
- Exon/intron boundaries
- Functional annotations

### WIG/BigWig

**File Extensions:** `.wig`, `.bw`, `.bigwig`

**Description:** Format for continuous-valued data (e.g., coverage, conservation scores).

**Formats:**
- **WIG** - Text format
- **BigWig** - Binary indexed format (faster)

## Clinical Data Formats

### HL7 v2 Messages

**File Extensions:** `.hl7`, `.txt`

**Description:** Standard for healthcare data exchange.

**Message Types:**
- ADT (Admission, Discharge, Transfer)
- ORM (Order messages)
- ORU (Observation results)
- MDM (Medical document management)

**Structure:**
```
MSH|^~\&|SendingApp|SendingFac|ReceivingApp|ReceivingFac|20240101120000||ADT^A01|MSG001|P|2.5
PID|1||12345^^^Hospital^MR||Doe^John^A||19800101|M|||123 Main St^^City^ST^12345
```

### FHIR (Fast Healthcare Interoperability Resources)

**File Extensions:** `.json`, `.xml`

**Description:** Modern standard for healthcare data exchange.

**Resource Types:**
- Patient
- Observation
- Condition
- Procedure
- MedicationRequest
- DiagnosticReport
- Bundle

**Example (JSON):**
```json
{
  "resourceType": "Patient",
  "id": "example",
  "name": [{
    "use": "official",
    "family": "Doe",
    "given": ["John"]
  }],
  "gender": "male",
  "birthDate": "1980-01-01"
}
```

### CDA (Clinical Document Architecture)

**File Extensions:** `.xml`

**Description:** XML-based standard for clinical documents.

**Document Types:**
- Discharge summaries
- Progress notes
- Consultation notes
- Operative reports

## Data Conversion

### Converting Between Formats

**DICOM to NIfTI:**
```python
import nibabel as nib
from container.medical-tools.dicom_utils import *

# Read DICOM series
series = read_dicom_series('/path/to/dicom')
volume, metadata = create_volume_from_series(series)

# Create NIfTI
affine = np.eye(4)
affine[:3, :3] = np.diag(metadata['spacing'])
nii_img = nib.Nifti1Image(volume, affine)
nib.save(nii_img, 'output.nii.gz')
```

**SAM to BAM:**
```bash
samtools view -bS input.sam > output.bam
samtools sort output.bam -o sorted.bam
samtools index sorted.bam
```

**VCF to BCF:**
```bash
bcftools view -O b input.vcf.gz > output.bcf
bcftools index output.bcf
```

## File Size Considerations

### Typical File Sizes

**Medical Imaging:**
- Single DICOM slice: 0.5-2 MB
- CT series (200 slices): 100-400 MB
- MRI series: 50-500 MB
- Whole slide image: 1-10 GB
- NIfTI brain volume: 10-100 MB

**Genomics:**
- FASTQ (human WGS): 50-200 GB
- BAM (human WGS): 50-150 GB
- VCF (human variants): 1-10 GB
- Reference genome: 3 GB

### Compression

**Recommended Compression:**
- DICOM: Usually uncompressed or JPEG
- NIfTI: Use `.nii.gz` (gzip compression)
- FASTQ: Use `.fastq.gz` (gzip compression)
- VCF: Use `.vcf.gz` with tabix index
- BAM: Already compressed

## Data Validation

### Checking File Integrity

**DICOM:**
```python
import pydicom
try:
    ds = pydicom.dcmread('file.dcm')
    print("Valid DICOM file")
except:
    print("Invalid DICOM file")
```

**NIfTI:**
```python
import nibabel as nib
try:
    img = nib.load('file.nii.gz')
    print(f"Valid NIfTI: {img.shape}")
except:
    print("Invalid NIfTI file")
```

**BAM:**
```bash
samtools quickcheck file.bam && echo "Valid BAM" || echo "Invalid BAM"
```

**VCF:**
```bash
bcftools view -H file.vcf.gz | head -1 && echo "Valid VCF" || echo "Invalid VCF"
```

## Best Practices

### Storage
- Use compressed formats when possible
- Organize by study/patient/modality
- Implement proper backup strategies
- Use encrypted storage for sensitive data

### Processing
- Validate files before processing
- Check for required metadata
- Handle missing data gracefully
- Document all transformations

### Sharing
- Anonymize patient data
- Use standard formats
- Include metadata and documentation
- Follow data sharing agreements

## Resources

### Format Specifications
- DICOM: https://www.dicomstandard.org/
- NIfTI: https://nifti.nimh.nih.gov/
- SAM/BAM: https://samtools.github.io/hts-specs/
- VCF: https://samtools.github.io/hts-specs/VCFv4.3.pdf
- FHIR: https://www.hl7.org/fhir/
- HL7 v2: https://www.hl7.org/implement/standards/product_brief.cfm?product_id=185

### Tools
- DICOM: dcm4che, DCMTK, pydicom
- NIfTI: nibabel, FSL, AFNI
- Genomics: samtools, bcftools, GATK
- FHIR: HAPI FHIR, fhir.resources
