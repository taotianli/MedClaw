# MedClaw Quick Start Guide

Get started with MedClaw in 5 minutes.

## Prerequisites

- macOS or Linux
- Node.js 20+
- Docker Desktop
- Claude Code CLI

## Installation

```bash
# Clone the repository
git clone https://github.com/taotianli/MedClaw.git
cd MedClaw

# Open Claude Code
claude
```

In Claude Code, run:
```
/setup
```

This will:
- Install dependencies
- Build the Docker container with medical tools
- Configure the service

## First Analysis

### Test DICOM Processing

```bash
# Create test directory
mkdir -p test_data

# In Claude Code:
@MedClaw I have a DICOM file at test_data/scan.dcm. Can you analyze it and tell me the modality, patient info, and image dimensions?
```

### Test Genomic Analysis

```bash
# In Claude Code:
@MedClaw I have a VCF file at test_data/variants.vcf. Can you parse it and show me variant statistics?
```

## Common Commands

### Analyze Medical Images

```
@MedClaw analyze the DICOM series in /data/ct_study and segment the liver
@MedClaw load the NIfTI file brain.nii.gz and calculate the brain volume
@MedClaw segment the tumor from this MRI scan and calculate its volume
```

### Process Genomic Data

```
@MedClaw parse this VCF file and filter variants with quality > 30
@MedClaw analyze the BAM file and show me mapping statistics
@MedClaw calculate GC content for sequences in this FASTA file
```

### Clinical Data

```
@MedClaw parse this FHIR Patient resource and extract demographics
@MedClaw convert this HL7 message to FHIR format
@MedClaw anonymize the patient data in this DICOM file
```

## Configuration

### Set Up Medical Data Directories

Edit `.env`:
```bash
MEDICAL_DATA_ROOT=/path/to/medical/data
DICOM_DATA_PATH=/path/to/dicom
GENOMICS_DATA_PATH=/path/to/genomics
```

### Increase Docker Memory

For large imaging datasets:

**macOS:**
Docker Desktop → Settings → Resources → Memory: 16GB

**Linux:**
```bash
# Edit /etc/docker/daemon.json
{
  "default-ulimits": {
    "memlock": {
      "Hard": -1,
      "Soft": -1
    }
  }
}
```

## Next Steps

- Read the [Medical Analysis Guide](MEDICAL_ANALYSIS_GUIDE.md) for detailed examples
- Review [Setup Guide](SETUP_GUIDE.md) for advanced configuration
- Check [Medical Data Formats](MEDICAL_DATA_FORMATS.md) for supported formats
- Join the [Discord community](https://discord.gg/VDdww8qS42)

## Troubleshooting

### Container Build Fails

```bash
# Clean Docker cache
docker system prune -a

# Rebuild
cd container
./build.sh
```

### Out of Memory

Increase Docker memory limits or process data in smaller chunks.

### Python Package Missing

```bash
# Enter container
docker run -it --rm medclaw-agent /bin/bash

# Install package
pip install package-name
```

## Getting Help

- Run `/debug` in Claude Code
- Check logs: `docker logs medclaw-agent`
- Ask in Discord: https://discord.gg/VDdww8qS42
- Open an issue: https://github.com/taotianli/MedClaw/issues
