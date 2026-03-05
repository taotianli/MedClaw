# MedClaw Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2026-03-05

### Added - Medical Focus
- **Medical Imaging Support**
  - DICOM file processing and analysis utilities
  - NIfTI neuroimaging data handling
  - Image segmentation tools using SimpleITK
  - Volume calculation and ROI analysis
  - Support for CT, MRI, and other medical imaging modalities

- **Genomic Analysis Tools**
  - VCF file parsing and variant analysis
  - BAM/SAM file processing and statistics
  - FASTA sequence analysis
  - Variant annotation and filtering
  - Coverage analysis utilities

- **Clinical Data Processing**
  - FHIR resource handling (Patient, Observation, Bundle)
  - HL7 v2 message parsing
  - Clinical data anonymization
  - Vital signs extraction

- **Medical Python Packages**
  - pydicom 2.4.4 - DICOM file handling
  - nibabel 5.2.1 - Neuroimaging data I/O
  - SimpleITK 2.3.1 - Image analysis and registration
  - scikit-image 0.22.0 - Image processing
  - BioPython 1.83 - Sequence analysis
  - pysam 0.22.0 - SAM/BAM manipulation
  - PyVCF3 1.0.3 - VCF parsing
  - fhir.resources 7.1.0 - FHIR handling
  - hl7apy 1.3.4 - HL7 message processing

- **Documentation**
  - Medical Analysis Guide with workflow examples
  - Setup Guide for medical data configuration
  - Security and compliance guidelines
  - Medical data format specifications

- **Utility Scripts**
  - `dicom_utils.py` - DICOM processing utilities
  - `nifti_utils.py` - NIfTI analysis utilities
  - `genomics_utils.py` - Genomic data utilities
  - `segmentation_utils.py` - Image segmentation utilities
  - `clinical_utils.py` - Clinical data utilities

### Changed
- Renamed from NanoClaw to MedClaw
- Updated assistant name from "Andy" to "MedClaw"
- Modified container image name to `medclaw-agent:latest`
- Updated configuration paths to use `medclaw` instead of `nanoclaw`
- Enhanced Dockerfile with medical analysis dependencies
- Updated README files with medical focus and capabilities

### Configuration
- Default assistant name: `MedClaw`
- Container image: `medclaw-agent:latest`
- Config directory: `~/.config/medclaw/`
- Recommended RAM: 16GB+ for medical imaging
- Python environment: `/opt/medclaw-env`

## Migration from NanoClaw

If you're migrating from NanoClaw:

1. **Update configuration paths:**
   ```bash
   mv ~/.config/nanoclaw ~/.config/medclaw
   ```

2. **Update environment variables:**
   ```bash
   # In .env file
   ASSISTANT_NAME=MedClaw
   CONTAINER_IMAGE=medclaw-agent:latest
   ```

3. **Rebuild container:**
   ```bash
   cd container
   ./build.sh
   ```

4. **Update service files:**
   - macOS: Update `~/Library/LaunchAgents/com.medclaw.plist`
   - Linux: Update systemd service file

## Security & Compliance

- Container isolation for patient data protection
- Data anonymization utilities included
- Audit logging capabilities
- HIPAA/GDPR compliance considerations documented
- Encrypted storage recommendations

## Known Issues

- Large medical imaging datasets (>10GB) may require increased Docker memory limits
- GPU acceleration for deep learning requires additional configuration
- Some medical file formats may require additional Python packages

## Future Enhancements

Planned features for future releases:

- **Advanced Imaging:**
  - MONAI integration for medical imaging AI
  - 3D Slicer integration
  - Whole slide imaging support (OpenSlide)
  - PACS integration

- **Genomics:**
  - GATK pipeline integration
  - RNA-seq analysis workflows
  - Single-cell analysis tools
  - Metagenomics support

- **Clinical Integration:**
  - EHR system connectors
  - Radiology reporting templates
  - Clinical decision support tools
  - Lab information system integration

## Contributing

We welcome contributions! Areas of interest:

- Medical analysis skills and workflows
- Additional medical data format support
- Performance optimizations
- Compliance and security enhancements
- Documentation improvements

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Acknowledgments

MedClaw is built on [NanoClaw](https://github.com/qwibitai/nanoclaw) and leverages the excellent work of the medical imaging and bioinformatics open source communities.

## License

MIT License - See [LICENSE](LICENSE) for details.

**Disclaimer:** MedClaw is provided for research and educational purposes. Not intended for clinical diagnosis or treatment decisions without proper validation and regulatory approval.

---

## Previous NanoClaw History

### [1.2.0](https://github.com/qwibitai/nanoclaw/compare/v1.1.6...v1.2.0)

[BREAKING] WhatsApp removed from core, now a skill. Run `/add-whatsapp` to re-add (existing auth/groups preserved).
- **fix:** Prevent scheduled tasks from executing twice when container runtime exceeds poll interval (#138, #669)
