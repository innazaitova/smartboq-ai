@echo off
REM QuantiBot AI - Quick Start Script for Windows
REM This script sets up and starts the QuantiBot AI platform

echo ==========================================
echo   QuantiBot AI - Quick Start
echo ==========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    echo    Visit: https://docs.docker.com/desktop/windows/install/
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

echo ✅ Docker and Docker Compose are installed
echo.

REM Check if .env file exists
if not exist "backend\.env" (
    echo ⚠️  No .env file found. Creating from template...
    copy "backend\.env.example" "backend\.env"
    echo.
    echo 📝 IMPORTANT: Edit backend\.env with your API keys:
    echo    - ANTHROPIC_API_KEY (get from https://console.anthropic.com^)
    echo    - JWT_SECRET_KEY (generate random 32-character string^)
    echo    - AWS credentials for S3
    echo    - Stripe keys for payments
    echo.
    pause
)

echo ✅ Environment configured
echo.

echo 🚀 Starting QuantiBot AI...
echo.

REM Build and start containers
docker-compose up -d --build

echo.
echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Check if services are running
docker-compose ps | findstr "Up" >nul
if errorlevel 1 (
    echo.
    echo ❌ Failed to start services. Check logs:
    echo    docker-compose logs
    pause
    exit /b 1
)

echo.
echo ==========================================
echo   ✅ QuantiBot AI is running!
echo ==========================================
echo.
echo 📱 Access the application:
echo    Frontend:  http://localhost:3000
echo    Backend:   http://localhost:8000
echo    API Docs:  http://localhost:8000/docs
echo.
echo 📊 View logs:
echo    docker-compose logs -f
echo.
echo 🛑 Stop application:
echo    docker-compose down
echo.
echo 📚 Next steps:
echo    1. Open http://localhost:3000 in your browser
echo    2. Create an account (free trial^)
echo    3. Upload a construction drawing
echo    4. Get your BOQ in 30 minutes!
echo.
echo 📖 Documentation: See README.md and DEPLOYMENT.md
echo.
pause
