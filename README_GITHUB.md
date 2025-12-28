# 🏗️ QuantiBot AI - AI-Powered Quantity Surveying

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![Next.js](https://img.shields.io/badge/next.js-14.1-black.svg)

Transform 20 hours of manual quantity surveying into 30 minutes with AI.

## ⚡ Quick Overview

- **40x Faster**: 30 minutes vs 20 hours
- **88% Cheaper**: $997/month vs $75,000/year
- **95% Accurate**: GPT-4o Vision AI

## 🚀 Quick Start

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/quantibot-ai.git
cd quantibot-ai

# Backend setup
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy env.example .env  # Configure with your credentials
python init_db.py

# Frontend setup
cd ../frontend
npm install
copy .env.example .env.local  # Configure API URL

# Run application
# Terminal 1: cd backend && uvicorn main:app --reload
# Terminal 2: cd frontend && npm run dev
```

Access: http://localhost:3000

## 📁 Project Structure

```
├── frontend/          # Next.js 14 App
├── backend/           # FastAPI Backend
├── ai-engine/         # AI Processing
└── database_schema.sql
```

## 🔧 Tech Stack

- **Frontend**: Next.js 14, React, Tailwind CSS
- **Backend**: FastAPI, PostgreSQL, SQLAlchemy
- **AI**: OpenAI GPT-4o Vision
- **Auth**: JWT, bcrypt

## ✅ Features

- ✅ User authentication
- ✅ Project management  
- ✅ File upload (PDF/DWG/images)
- ✅ AI drawing analysis
- ✅ Responsive dashboard
- 🚧 BOQ generation
- 🚧 Cost estimation

## 🚀 Deployment

See [PRODUCTION_DEPLOY.md](PRODUCTION_DEPLOY.md)

- Frontend: Vercel (free)
- Backend: Railway ($5/month)
- Database: Railway Postgres ($7/month)

## ⚠️ Before Deploying

1. Read [SECURITY_README.md](SECURITY_README.md)
2. Never commit `.env` files
3. Generate secure JWT secret
4. Update ALLOWED_ORIGINS
5. Configure production database

## 📄 License

MIT License

## 📞 Contact

Email: support@quantibot.ai

---

Built in Karachi 🇵🇰 | Serving the World 🌍
