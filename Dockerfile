FROM nvcr.io/nvidia/l4t-ml:r36.2.0-py3

# Set working directory
WORKDIR /home/extra

# Install system dependencies
RUN apt update && apt install -y \
    python3.10-venv \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Note: Project files are mounted by devcontainer, not copied
# The devcontainer.json already has: "workspaceMount": "source=${localWorkspaceFolder},target=/home/extra,type=bind,consistency=cached"

# Expose any necessary ports (if needed)
# EXPOSE 8080

# Default command
CMD ["/bin/bash"]
