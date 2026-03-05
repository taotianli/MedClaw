<p align="center">
  <img src="assets/nanoclaw-logo.png" alt="MedClaw" width="400">
</p>

<p align="center">
  An AI-powered medical analysis assistant for medical imaging and genomic data. Built on secure containerized agents with specialized tools for healthcare research and clinical workflows.
</p>

<p align="center">
  <a href="README_zh.md">中文</a>&nbsp; • &nbsp;
  <a href="https://discord.gg/VDdww8qS42"><img src="https://img.shields.io/discord/1470188214710046894?label=Discord&logo=discord&v=2" alt="Discord" valign="middle"></a>
</p>

MedClaw leverages Claude Code to provide intelligent analysis of medical imaging (DICOM, NIfTI, microscopy) and genomic data (VCF, FASTQ, BAM), with support for clinical workflows and research pipelines.

## Why MedClaw

Medical data analysis requires specialized tools, secure handling of sensitive patient information, and integration with clinical workflows. MedClaw provides:

- **Secure isolation** - Patient data stays in containerized environments with filesystem isolation
- **Medical imaging support** - DICOM, NIfTI, whole slide imaging, and microscopy analysis
- **Genomic analysis** - Variant calling, sequence alignment, gene expression analysis
- **Clinical integration** - HL7/FHIR support, EHR integration capabilities
- **Research workflows** - Batch processing, pipeline automation, reproducible analysis
- **Lightweight architecture** - Small codebase you can understand and audit for compliance

## Quick Start

```bash
git clone https://github.com/taotianli/MedClaw.git
cd MedClaw
claude
```

Then run `/setup`. Claude Code handles dependencies, medical tool installation, container setup, and service configuration.

> **Note:** Commands prefixed with `/` (like `/setup`) are [Claude Code skills](https://code.claude.com/docs/en/skills). Type them inside the `claude` CLI prompt.

See [Quick Start Guide](docs/QUICK_START.md) for detailed instructions.

## Medical Capabilities

### Medical Imaging
- **DICOM processing** - Read, analyze, and convert DICOM files
- **NIfTI analysis** - Brain imaging, fMRI, structural MRI processing
- **Whole slide imaging** - Digital pathology, histology analysis
- **Image segmentation** - Organ, tumor, and tissue segmentation
- **3D reconstruction** - CT/MRI volume rendering and analysis
- **Image registration** - Multi-modal image alignment

### Genomic Analysis
- **Variant analysis** - VCF parsing, annotation, filtering
- **Sequence alignment** - BAM/SAM file processing, quality control
- **Gene expression** - RNA-seq analysis, differential expression
- **Genome assembly** - De novo assembly, scaffolding
- **Phylogenetic analysis** - Tree building, evolutionary analysis
- **Annotation** - Gene prediction, functional annotation

### Clinical Tools
- **HL7/FHIR** - Healthcare data exchange standards
- **EHR integration** - Electronic health record connectivity
- **Clinical decision support** - Evidence-based recommendations
- **Report generation** - Structured clinical reports
- **Data anonymization** - HIPAA-compliant de-identification

## Medical Tools & Libraries

MedClaw includes pre-configured medical analysis tools:

**Imaging:**
- pydicom - DICOM file handling
- nibabel - Neuroimaging data I/O
- SimpleITK - Image analysis and registration
- scikit-image - Image processing algorithms
- OpenSlide - Whole slide imaging
- 3D Slicer integration - Advanced visualization

**Genomics:**
- BioPython - Sequence analysis
- pysam - SAM/BAM file manipulation
- PyVCF - VCF file parsing
- scikit-bio - Bioinformatics algorithms
- GATK integration - Variant calling pipelines
- Samtools/BCFtools - Sequence data processing

**Machine Learning:**
- TensorFlow/PyTorch - Deep learning frameworks
- MONAI - Medical imaging AI toolkit
- DeepVariant - Genomic variant calling
- nnU-Net - Medical image segmentation

**Clinical:**
- FHIR-py - FHIR resource handling
- HL7apy - HL7 message processing
- Presidio - Data anonymization

## Usage Examples

Talk to your medical assistant with the trigger word (default: `@MedClaw`):

```
@MedClaw analyze this DICOM series and identify any abnormalities in the CT scan
@MedClaw process these VCF files and generate a variant report for pathogenic mutations
@MedClaw segment the tumor regions from this MRI scan and calculate volumes
@MedClaw align these RNA-seq reads and perform differential expression analysis
@MedClaw convert this whole slide image to a pyramidal TIFF and extract tissue regions
@MedClaw every Monday at 8am, check for new imaging studies and generate quality control reports
```

From the main channel, manage analysis workflows:
```
@MedClaw list all scheduled genomic pipeline tasks
@MedClaw pause the weekly imaging QC task
@MedClaw show me the status of the variant calling pipeline
```

## Documentation

- [Quick Start Guide](docs/QUICK_START.md) - Get started in 5 minutes
- [Setup Guide](docs/SETUP_GUIDE.md) - Detailed installation and configuration
- [Medical Analysis Guide](docs/MEDICAL_ANALYSIS_GUIDE.md) - Workflow examples and tutorials
- [Medical Data Formats](docs/MEDICAL_DATA_FORMATS.md) - Supported file formats
- [Security & Compliance](docs/SECURITY.md) - HIPAA/GDPR considerations

## Security & Compliance

**HIPAA Considerations:**
- Container isolation protects patient data
- Audit logging for all data access
- Data anonymization tools included
- Encrypted storage recommendations
- Access control via filesystem mounts

**Best Practices:**
- Review the codebase for compliance requirements
- Configure appropriate data retention policies
- Use encrypted volumes for sensitive data
- Implement proper authentication for channels
- Regular security audits

See [docs/SECURITY.md](docs/SECURITY.md) for detailed security model.

## Customizing

MedClaw is designed to be customized for your specific medical workflows:

- "Add support for analyzing PET/CT fusion images"
- "Integrate with our hospital's PACS system"
- "Create a pipeline for automated lung nodule detection"
- "Add support for single-cell RNA-seq analysis"
- "Generate structured radiology reports in our template format"

Or run `/customize` for guided changes.

## Architecture

```
Channels --> SQLite --> Polling loop --> Container (Claude Agent SDK + Medical Tools) --> Response
```

Single Node.js process with medical analysis tools running in isolated containers. Only mounted medical data directories are accessible. Per-group message queue with concurrency control.

Key files:
- `src/index.ts` - Orchestrator: state, message loop, agent invocation
- `src/channels/registry.ts` - Channel registry (self-registration)
- `src/container-runner.ts` - Spawns agent containers with medical tools
- `container/medical-tools/` - Medical imaging and genomics tool configurations
- `groups/*/CLAUDE.md` - Per-group medical context and memory

For full architecture details, see [docs/SPEC.md](docs/SPEC.md).

## Medical Data Formats Supported

**Imaging:**
- DICOM (.dcm, .dicom)
- NIfTI (.nii, .nii.gz)
- NRRD (.nrrd)
- Analyze (.hdr, .img)
- TIFF/BigTIFF (.tif, .tiff)
- SVS, NDPI (whole slide formats)

**Genomics:**
- FASTQ (.fastq, .fq, .fastq.gz)
- FASTA (.fasta, .fa, .fna)
- SAM/BAM/CRAM (.sam, .bam, .cram)
- VCF/BCF (.vcf, .vcf.gz, .bcf)
- GFF/GTF (.gff, .gtf)
- BED (.bed)

**Clinical:**
- HL7 v2 messages
- FHIR JSON/XML
- CDA documents

See [docs/MEDICAL_DATA_FORMATS.md](docs/MEDICAL_DATA_FORMATS.md) for complete format specifications.

## Requirements

- macOS or Linux
- Node.js 20+
- [Claude Code](https://claude.ai/download)
- [Docker](https://docker.com/products/docker-desktop) (for container isolation)
- Python 3.9+ (for medical analysis tools)
- 16GB+ RAM recommended for imaging analysis
- GPU recommended for deep learning tasks

## Contributing

**Add medical analysis skills, not features.**

Contribute skills that teach Claude Code how to add medical capabilities:

- `/add-pacs-integration` - Connect to PACS systems
- `/add-pathology-viewer` - Whole slide image viewer
- `/add-variant-pipeline` - Automated variant calling
- `/add-dicom-router` - DICOM networking and routing
- `/add-clinical-nlp` - Extract information from clinical notes

### RFS (Request for Skills)

Medical skills we'd like to see:

**Imaging Analysis**
- `/add-brain-segmentation` - Automated brain structure segmentation
- `/add-lung-nodule-detection` - CT lung nodule detection pipeline
- `/add-cardiac-analysis` - Cardiac MRI analysis tools

**Genomics**
- `/add-somatic-pipeline` - Cancer somatic variant calling
- `/add-rna-seq-pipeline` - Complete RNA-seq analysis workflow
- `/add-metagenomics` - Microbiome analysis tools

**Clinical Integration**
- `/add-ehr-connector` - EHR system integration
- `/add-radiology-reporting` - Structured report generation
- `/add-clinical-trials` - Clinical trial data management

## FAQ

**Is this HIPAA compliant?**

MedClaw provides technical safeguards (container isolation, audit logging, encryption support), but HIPAA compliance requires organizational policies, business associate agreements, and proper implementation. Review the codebase and implement appropriate controls for your use case.

**Can I use this for clinical diagnosis?**

MedClaw is a research and analysis tool. Any clinical use requires proper validation, regulatory approval, and oversight by qualified healthcare professionals. Always follow applicable regulations and guidelines.

**What about data privacy?**

All analysis runs in isolated containers. Patient data never leaves your system unless you explicitly configure external integrations. Use encrypted storage and proper access controls.

**Can I integrate with our hospital systems?**

Yes. MedClaw can be customized to integrate with PACS, EHR, LIS, and other clinical systems. Use skills or custom code to add integrations.

**How do I process large imaging datasets?**

Configure appropriate mount points for your data storage, use batch processing workflows, and consider GPU acceleration for deep learning tasks. The container system supports mounting network storage and high-performance filesystems.

## Community

Questions? Ideas? [Join the Discord](https://discord.gg/VDdww8qS42).

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and migration notes.

## License

MIT

**Disclaimer:** MedClaw is provided for research and educational purposes. Not intended for clinical diagnosis or treatment decisions without proper validation and regulatory approval. Users are responsible for compliance with applicable healthcare regulations including HIPAA, GDPR, and local laws.

## Acknowledgments

MedClaw is built on [NanoClaw](https://github.com/qwibitai/nanoclaw) and leverages the excellent work of the medical imaging and bioinformatics open source communities.
