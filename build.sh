#!/bin/bash

# Exit immediately on any error
set -e

# Wait for user input before exiting
wait_exit() {
  echo -e "\nPress enter to exit..."
  read -r
  exit
}

# Utility to safely change directories
safe_cd() {
  cd "$1" || { echo "❌ Failed to enter directory: $1"; wait_exit; }
}

# -----------------------------
# 🔧 Build: Node.js Backend (bot)
# -----------------------------
echo -e "\n🚀 Building Node.js backend (bot)..."

safe_cd bot
npm install
npm run build || wait_exit

# ⚠️ Copy .env into the build directory
echo -e "⚠️  Copying .env to build folder..."
cp ./.env ./build/.env

cd ..

# -------------------------------
# 💻 Build: Frontend (uses bot API)
# -------------------------------
echo -e "\n🌐 Building frontend..."

safe_cd frontend
npm install
npm run build || wait_exit
cd ..

# --------------------------------------
# 🐳 Docker: Build and start containers
# --------------------------------------
echo -e "\n📦 Building Docker images and starting containers..."
docker compose up --build -d --scale scraper=3 || wait_exit

echo -e "\n✅ Build Complete!"
wait_exit
