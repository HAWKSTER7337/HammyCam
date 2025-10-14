FROM python:3.11-slim-bullseye

# Avoid warnings by switching to noninteractive
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies for OpenCV, camera support, and virtual camera
RUN apt-get update && apt-get install -y \
    # Build essentials
    build-essential \
    cmake \
    pkg-config \
    # Video and camera libraries
    libv4l-dev \
    v4l-utils \
    # OpenCV dependencies
    libopencv-dev \
    python3-opencv \
    # Image processing libraries
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    # GUI support (optional, for displaying video)
    libgtk-3-dev \
    libcanberra-gtk3-module \
    # Virtual camera support
    ffmpeg \
    # Utilities
    git \
    wget \
    curl \
    sudo \
    # Clean up
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create a non-root user
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Add user to video group for camera access
RUN usermod -aG video $USERNAME

# Set up Python environment
RUN pip install --upgrade pip setuptools wheel

# Switch back to interactive mode
ENV DEBIAN_FRONTEND=dialog

# Set the default user
USER $USERNAME

WORKDIR /workspaces/HammyCam

