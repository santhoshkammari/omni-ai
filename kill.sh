#!/bin/bash

# Stop all running containers
echo "Stopping all running Docker containers..."
docker stop $(docker ps -aq)

# Remove all containers
echo "Removing all Docker containers..."
docker rm $(docker ps -aq)

# Optional: Remove all images
# Uncomment the next two lines if you want to remove all Docker images as well
# echo "Removing all Docker images..."
# docker rmi $(docker images -q)

echo "Cleanup complete."