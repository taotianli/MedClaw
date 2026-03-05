# MedClaw Installation and Setup Guide

This guide walks you through setting up MedClaw for medical data analysis.

## Prerequisites

### System Requirements

- **Operating System**: macOS or Linux
- **RAM**: 16GB minimum (32GB+ recommended for large imaging datasets)
- **Storage**: 50GB+ free space for medical data and container images
- **GPU**: Optional but recommended for deep learning tasks

### Software Requirements

- **Node.js**: Version 20 or higher
- **Docker**: Docker Desktop (macOS/Linux) or Docker Engine (Linux)
- **Claude Code**: Latest version from [claude.ai/download](https://claude.ai/download)
- **Python**: 3.9+ (installed automatically in container)
- **Git**: For cloning the repository

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/taotianli/MedClaw.git
cd MedClaw
```

### 2. Run Setup

Open Claude Code in the MedClaw directory:

```bash
claude
```

Then run the setup skill:

```
/setup
```

Claude Code will guide you through:
- Installing Node.js dependencies
- Building the Docker container with medical tools
- Configuring authentication for messaging channels
- Setting up the background service

### 3. Verify Installation

Check that medical tools are available:

```bash
# Build the container
./container/build.sh

# Verify Python packages are installed
docker run --rm medclaw-agent python3 -c "import pydicom, nibabel, pysam; print('Medical tools installed successfully')"
```

## Configuration

### Medical Data Directories

Configure mount points for your medical data in your group's configuration:

```bash
# Create a group for medical analysis
mkdir -p groups/medical-imaging
```

Edit `groups/medical-imaging/CLAUDE.md`:

```markdown
# Medical Imaging Group

This group has access to medical imaging data.

## Mounted Directories
- `/data/dicom` - DICOM imaging studies
- `/data/nifti` - NIfTI brain imaging data
- `/data/genomics` - Genomic data files
```

### Environment Variables

Create a `.env` file in the MedClaw root directory:

```bash
# Anthropic API Configuration
ANTHROPIC_API_KEY=your_api_key_here

# Optional: Custom model endpoint
# ANTHROPIC_BASE_URL=https://your-endpoint.com
# ANTHROPIC_AUTH_TOKEN=your-token

# Container Configuration
CONTAINER_MEMORY_LIMIT=16g
CONTAINER_CPU_LIMIT=4

# Medical Data Paths (adjust to your setup)
MEDICAL_DATA_ROOT=/path/to/medical/data
DICOM_DATA_PATH=/path/to/dicom/studies
GENOMICS_DATA_PATH=/path/to/genomics/data
```

### Docker Resource Limits

For medical imaging analysis, increase Docker resource limits:

**macOS (Docker Desktop):**
1. Open Docker Desktop
2. Go to Settings → Resources
3. Set Memory to 16GB+ and CPUs to 4+
4. Click "Apply & Restart"

**Linux:**
Edit `/etc/docker/daemon.json`:

```json
{
  "default-runtime": "runc",
  "default-ulimits": {
    "memlock": {
      "Hard": -1,
      "Name": "memlock",
      "Soft": -1
    }
  }
}
```

Restart Docker:
```bash
sudo systemctl restart docker
```

## Adding Medical Tools

### Installing Additional Python Packages

Edit `container/Dockerfile` to add more medical packages:

```dockerfile
RUN /opt/medclaw-env/bin/pip install --no-cache-dir \
    # Add your packages here
    monai==1.3.0 \
    nilearn==0.10.3 \
    pyradiomics==3.1.0 \
    openslide-python==1.3.1
```

Rebuild the container:

```bash
./container/build.sh
```

### Common Medical Packages

**Advanced Imaging:**
- `monai` - Medical imaging AI toolkit
- `nilearn` - Neuroimaging machine learning
- `pyradiomics` - Radiomics feature extraction
- `openslide-python` - Whole slide imaging

**Genomics:**
- `pybedtools` - BED file manipulation
- `cyvcf2` - Fast VCF parsing
- `scikit-allel` - Population genetics

**Deep Learning:**
- `torch` - PyTorch
- `tensorflow` - TensorFlow
- `nnunet` - Medical image segmentation

## Channel Setup

### WhatsApp Integration

Add WhatsApp for mobile access to medical analysis:

```
/add-whatsapp
```

Follow the prompts to authenticate with QR code or pairing code.

### Telegram Integration

Add Telegram for secure messaging:

```
/add-telegram
```

Provide your Telegram bot token when prompted.

### Slack Integration

Add Slack for team collaboration:

```
/add-slack
```

Configure Slack Socket Mode credentials.

## Data Security Setup

### Encrypted Storage

Use encrypted volumes for sensitive medical data:

**macOS:**
```bash
# Create encrypted disk image
hdiutil create -size 100g -encryption AES-256 -volname "MedicalData" -fs APFS medical_data.dmg

# Mount encrypted volume
hdiutil attach medical_data.dmg
```

**Linux (LUKS):**
```bash
# Create encrypted volume
sudo cryptsetup luksFormat /dev/sdX
sudo cryptsetup open /dev/sdX medical_data

# Create filesystem
sudo mkfs.ext4 /dev/mapper/medical_data

# Mount
sudo mount /dev/mapper/medical_data /mnt/medical_data
```

### Access Control

Configure filesystem permissions:

```bash
# Restrict access to medical data directory
chmod 700 /path/to/medical/data
chown $USER:$USER /path/to/medical/data

# Set up group access if needed
sudo groupadd medical-users
sudo usermod -a -G medical-users $USER
sudo chgrp -R medical-users /path/to/medical/data
sudo chmod -R 770 /path/to/medical/data
```

### Audit Logging

Enable audit logging for data access:

```bash
# Linux: Enable auditd
sudo apt-get install auditd
sudo auditctl -w /path/to/medical/data -p rwxa -k medical_data_access

# View audit logs
sudo ausearch -k medical_data_access
```

## Testing the Installation

### Test DICOM Processing

```bash
# Download sample DICOM data
wget https://www.rubomedical.com/dicom_files/chest.zip
unzip chest.zip -d test_data/dicom

# Test with MedClaw
claude
```

In Claude Code:
```
@MedClaw analyze the DICOM files in test_data/dicom and provide a summary
```

### Test Genomic Analysis

```bash
# Download sample VCF
wget https://ftp.1000genomes.ebi.ac.uk/vol1/ftp/release/20130502/supporting/vcf_with_sample_level_annotation/ALL.chr22.phase3_shapeit2_mvncall_integrated_v5b.20130502.genotypes.vcf.gz

# Test with MedClaw
```

In Claude Code:
```
@MedClaw parse this VCF file and show me variant statistics
```

## Troubleshooting

### Container Build Fails

If the container build fails due to package installation:

```bash
# Clean Docker cache
docker system prune -a

# Rebuild with no cache
cd container
./build.sh --no-cache
```

### Out of Memory Errors

Increase Docker memory limits or process data in smaller chunks:

```python
# Process large volumes in slices
for i in range(0, volume.shape[0], 10):
    slice_batch = volume[i:i+10]
    # Process batch
```

### Python Package Conflicts

If you encounter package version conflicts:

```bash
# Enter container shell
docker run -it --rm medclaw-agent /bin/bash

# Check installed packages
pip list

# Reinstall specific package
pip install --force-reinstall package-name==version
```

### Permission Denied Errors

Ensure proper permissions on mounted directories:

```bash
# Check permissions
ls -la /path/to/medical/data

# Fix permissions
sudo chown -R $USER:$USER /path/to/medical/data
chmod -R 755 /path/to/medical/data
```

## Next Steps

- Read the [Medical Analysis Guide](MEDICAL_ANALYSIS_GUIDE.md) for usage examples
- Review [Security Best Practices](SECURITY.md) for HIPAA compliance
- Explore the [API Documentation](API.md) for custom integrations
- Join the [Discord community](https://discord.gg/VDdww8qS42) for support

## Getting Help

If you encounter issues:

1. Run `/debug` in Claude Code for diagnostic information
2. Check the logs: `docker logs medclaw-agent`
3. Review the [troubleshooting guide](DEBUG_CHECKLIST.md)
4. Ask in the Discord community
5. Open an issue on GitHub

## Updating MedClaw

To update to the latest version:

```bash
# Pull latest changes
git pull origin main

# Rebuild container with updated medical tools
./container/build.sh

# Restart service
systemctl --user restart medclaw  # Linux
# or
launchctl kickstart -k gui/$(id -u)/com.medclaw  # macOS
```
