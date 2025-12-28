#!/bin/bash

# QuantiBot AI - Quick Start Script
# This script sets up and starts the QuantiBot AI platform

echo "=========================================="
echo "  QuantiBot AI - Quick Start"
echo "=========================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp backend/.env.example backend/.env
    echo ""
    echo "📝 IMPORTANT: Edit backend/.env with your API keys:"
    echo "   - ANTHROPIC_API_KEY (get from https://console.anthropic.com)"
    echo "   - JWT_SECRET_KEY (generate with: openssl rand -hex 32)"
    echo "   - AWS credentials for S3"
    echo "   - Stripe keys for payments"
    echo ""
    read -p "Press Enter after you've configured backend/.env..."
fi

echo "✅ Environment configured"
echo ""

# Generate JWT secret if needed
if grep -q "your-secret-key-minimum-32-characters-random" backend/.env; then
    echo "🔑 Generating JWT secret key..."
    SECRET=$(openssl rand -hex 32)
    sed -i "s/your-secret-key-minimum-32-characters-random/$SECRET/" backend/.env
    echo "✅ JWT secret generated"
fi

echo ""
echo "🚀 Starting QuantiBot AI..."
echo ""

# Build and start containers
docker-compose up -d --build

echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "=========================================="
    echo "  ✅ QuantiBot AI is running!"
    echo "=========================================="
    echo ""
    echo "📱 Access the application:"
    echo "   Frontend:  http://localhost:3000"
    echo "   Backend:   http://localhost:8000"
    echo "   API Docs:  http://localhost:8000/docs"
    echo ""
    echo "📊 View logs:"
    echo "   docker-compose logs -f"
    echo ""
    echo "🛑 Stop application:"
    echo "   docker-compose down"
    echo ""
    echo "📚 Next steps:"
    echo "   1. Open http://localhost:3000 in your browser"
    echo "   2. Create an account (free trial)"
    echo "   3. Upload a construction drawing"
    echo "   4. Get your BOQ in 30 minutes!"
    echo ""
    echo "📖 Documentation: See README.md and DEPLOYMENT.md"
    echo ""
else
    echo ""
    echo "❌ Failed to start services. Check logs:"
    echo "   docker-compose logs"
    exit 1
fi
