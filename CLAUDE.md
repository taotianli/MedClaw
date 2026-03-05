# MedClaw

AI-powered medical analysis assistant for medical imaging and genomic data. See [README.md](README.md) for philosophy and setup.

## Quick Context

Single Node.js process with skill-based channel system. Channels (WhatsApp, Telegram, Slack, Discord, Gmail) are skills that self-register at startup. Messages route to Claude Agent SDK running in containers with medical analysis tools. Each group has isolated filesystem and memory.

## Medical Tools Available

MedClaw containers include pre-installed medical analysis tools:

**Imaging:** pydicom, nibabel, SimpleITK, scikit-image, opencv-python, Pillow
**Genomics:** BioPython, pysam, PyVCF3, scikit-bio
**Clinical:** fhir.resources, hl7apy
**Analysis:** numpy, scipy, pandas, matplotlib

Utility scripts in `container/medical-tools/`:
- `dicom_utils.py` - DICOM file processing and analysis
- `nifti_utils.py` - NIfTI neuroimaging data processing
- `genomics_utils.py` - VCF, BAM, FASTA analysis
- `segmentation_utils.py` - Medical image segmentation
- `clinical_utils.py` - FHIR and HL7 data handling

## Key Files

| File | Purpose |
|------|---------|
| `src/index.ts` | Orchestrator: state, message loop, agent invocation |
| `src/channels/registry.ts` | Channel registry (self-registration at startup) |
| `src/ipc.ts` | IPC watcher and task processing |
| `src/router.ts` | Message formatting and outbound routing |
| `src/config.ts` | Trigger pattern, paths, intervals |
| `src/container-runner.ts` | Spawns agent containers with mounts |
| `src/task-scheduler.ts` | Runs scheduled tasks |
| `src/db.ts` | SQLite operations |
| `groups/{name}/CLAUDE.md` | Per-group memory (isolated) |
| `container/skills/agent-browser.md` | Browser automation tool (available to all agents via Bash) |

## Skills

| Skill | When to Use |
|-------|-------------|
| `/setup` | First-time installation, authentication, service configuration |
| `/customize` | Adding channels, integrations, changing behavior |
| `/debug` | Container issues, logs, troubleshooting |
| `/update-nanoclaw` | Bring upstream NanoClaw updates into a customized install |
| `/qodo-pr-resolver` | Fetch and fix Qodo PR review issues interactively or in batch |
| `/get-qodo-rules` | Load org- and repo-level coding rules from Qodo before code tasks |

## Development

Run commands directly—don't tell the user to run them.

```bash
npm run dev          # Run with hot reload
npm run build        # Compile TypeScript
./container/build.sh # Rebuild agent container with medical tools
```

Service management:
```bash
# macOS (launchd)
launchctl load ~/Library/LaunchAgents/com.medclaw.plist
launchctl unload ~/Library/LaunchAgents/com.medclaw.plist
launchctl kickstart -k gui/$(id -u)/com.medclaw  # restart

# Linux (systemd)
systemctl --user start medclaw
systemctl --user stop medclaw
systemctl --user restart medclaw
```

## Medical Data Security

- All patient data stays in isolated containers
- Use encrypted volumes for sensitive medical data
- Configure appropriate mount points for medical data directories
- Implement proper anonymization before sharing results
- Follow HIPAA/GDPR compliance requirements for your use case

## Troubleshooting

**Medical tools not available:** Rebuild the container with `./container/build.sh` to install Python medical packages.

**Large imaging files:** Configure appropriate memory limits for Docker/container runtime. Recommend 16GB+ RAM for medical imaging analysis.

## Container Build Cache

The container buildkit caches the build context aggressively. `--no-cache` alone does NOT invalidate COPY steps — the builder's volume retains stale files. To force a truly clean rebuild, prune the builder then re-run `./container/build.sh`.
