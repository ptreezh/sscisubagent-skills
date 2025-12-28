#!/bin/bash
# build-stigmergy-desktop.sh
# Script to build the Stigmergy Desktop Application
# This script will work when network access is available

set -e  # Exit immediately if a command exits with a non-zero status

echo "Building Stigmergy Desktop Application..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed. Please install Node.js before proceeding."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "npm is not installed. Please install npm before proceeding."
    exit 1
fi

echo "Node.js and npm are installed."

# Install dependencies
echo "Installing dependencies..."
npm install

# Verify the application functionality before building
echo "Verifying application functionality..."
npm test

# Build the application
echo "Building the application..."
npm run build

echo "Build completed successfully!"
echo "The distributable files are located in the 'dist/' directory."