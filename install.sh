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

# Prompt for Hugging Face credentials
read -p "Enter your Hugging Face email: " hf_email
read -sp "Enter your Hugging Face password: " hf_password
echo

# Create .env file
echo "HUGGINGFACE_EMAIL=$hf_email" > .env
echo "HUGGINGFACE_PASSWD=$hf_password" >> .env

# Build and start the Docker container
if ! docker-compose up --build -d; then
  echo "Docker build failed. Exiting."
  exit 1
fi


echo "Omni AI is now running. You can access it at http://localhost:8501"