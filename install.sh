#!/bin/bash

# Check if Docker is installed
if ! command -v docker &> /dev/null
then
    echo "Docker is not installed. Please install Docker and try again."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null
then
    echo "Docker Compose is not installed. Please install Docker Compose and try again."
    exit 1
fi


# Build and start the Docker container
if ! docker-compose up --build -d; then
  echo "Docker build failed. Exiting."
  exit 1
fi


echo "Omni AI is now running. You can access it at http://localhost:8501"
