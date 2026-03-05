# MedClaw Agent Container
# Runs Claude Agent SDK with medical imaging and genomics tools

FROM node:22-slim

# Install system dependencies for Chromium and medical tools
RUN apt-get update && apt-get install -y \
    chromium \
    fonts-liberation \
    fonts-noto-cjk \
    fonts-noto-color-emoji \
    libgbm1 \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libasound2 \
    libpangocairo-1.0-0 \
    libcups2 \
    libdrm2 \
    libxshmfence1 \
    curl \
    git \
    python3 \
    python3-pip \
    python3-venv \
    build-essential \
    libbz2-dev \
    liblzma-dev \
    zlib1g-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Set Chromium path for agent-browser
ENV AGENT_BROWSER_EXECUTABLE_PATH=/usr/bin/chromium
ENV PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium

# Install agent-browser and claude-code globally
RUN npm install -g agent-browser @anthropic-ai/claude-code

# Create Python virtual environment and install medical packages
RUN python3 -m venv /opt/medclaw-env && \
    /opt/medclaw-env/bin/pip install --no-cache-dir \
    # Medical Imaging
    pydicom==2.4.4 \
    nibabel==5.2.1 \
    SimpleITK==2.3.1 \
    scikit-image==0.22.0 \
    opencv-python-headless==4.9.0.80 \
    Pillow==10.2.0 \
    # Genomics
    biopython==1.83 \
    pysam==0.22.0 \
    PyVCF3==1.0.3 \
    scikit-bio==0.6.0 \
    # Machine Learning
    numpy==1.26.4 \
    scipy==1.12.0 \
    pandas==2.2.0 \
    matplotlib==3.8.2 \
    # Clinical Data
    fhir.resources==7.1.0 \
    hl7apy==1.3.4 \
    # Utilities
    requests==2.31.0 \
    pyyaml==6.0.1

# Add Python environment to PATH
ENV PATH="/opt/medclaw-env/bin:$PATH"
ENV VIRTUAL_ENV="/opt/medclaw-env"

# Create app directory
WORKDIR /app

# Copy package files first for better caching
COPY agent-runner/package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY agent-runner/ ./

# Copy medical tools
COPY medical-tools/ /app/medical-tools/

# Build TypeScript
RUN npm run build

# Create workspace directories
RUN mkdir -p /workspace/group /workspace/global /workspace/extra /workspace/ipc/messages /workspace/ipc/tasks /workspace/ipc/input

# Create entrypoint script
# Secrets are passed via stdin JSON — temp file is deleted immediately after Node reads it
# Follow-up messages arrive via IPC files in /workspace/ipc/input/
RUN printf '#!/bin/bash\nset -e\ncd /app && npx tsc --outDir /tmp/dist 2>&1 >&2\nln -s /app/node_modules /tmp/dist/node_modules\nchmod -R a-w /tmp/dist\ncat > /tmp/input.json\nnode /tmp/dist/index.js < /tmp/input.json\n' > /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Set ownership to node user (non-root) for writable directories
RUN chown -R node:node /workspace && chmod 777 /home/node

# Switch to non-root user (required for --dangerously-skip-permissions)
USER node

# Set working directory to group workspace
WORKDIR /workspace/group

# Entry point reads JSON from stdin, outputs JSON to stdout
ENTRYPOINT ["/app/entrypoint.sh"]
