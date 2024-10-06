#!/bin/bash

# Update package list
sudo apt update

# Install Git
sudo apt install -y git

# Install Docker
sudo apt install -y docker.io

# Install Docker Compose
sudo apt install -y docker-compose

# Add current user to docker group
sudo usermod -aG docker $USER

echo "Installation complete. Please log out and log back in for the changes to take effect."