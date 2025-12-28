# QuantiBot AI - Requirements & Setup

## System Requirements

### Development Environment
- **OS:** Windows 10/11, macOS 12+, or Linux (Ubuntu 20.04+)
- **RAM:** 16GB minimum, 32GB recommended
- **Storage:** 50GB free space
- **Internet:** Stable connection for API calls

### Required Software
```
Python 3.11+
Node.js 18+ & npm
PostgreSQL 14+
Git
Docker (optional, for deployment)
```

---

## Installation Guide

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/quantibot-ai.git
cd quantibot-ai
```

### 2. Backend Setup

#### Install Python Dependencies
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

#### Environment Variables
Create `.env` file in `/backend`:
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/quantibot
DB_HOST=localhost
DB_PORT=5432
DB_NAME=quantibot
DB_USER=postgres
DB_PASSWORD=yourpassword

# API Keys
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_CLOUD_VISION_KEY=your_gcp_key_here (optional)

# Authentication
JWT_SECRET_KEY=your_jwt_secret_here_generate_random_string
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# Storage (AWS S3 or local)
STORAGE_TYPE=s3  # or 'local'
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
AWS_BUCKET_NAME=quantibot-drawings
AWS_REGION=us-east-1

# Email (for notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# Environment
ENVIRONMENT=development  # or production
API_BASE_URL=http://localhost:8000
FRONTEND_URL=http://localhost:3000
```

#### Database Setup
```bash
# Create database
createdb quantibot

# Run migrations
python database_setup.py
```

### 3. Frontend Setup

#### Install Node Dependencies
```bash
cd ../frontend
npm install
```

#### Environment Variables
Create `.env.local` file in `/frontend`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_STRIPE_PUBLIC_KEY=your_stripe_key
```

### 4. Run Development Servers

#### Terminal 1 - Backend
```bash
cd backend
uvicorn main:app --reload --port 8000
```

#### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

Access application at: `http://localhost:3000`
Access API docs at: `http://localhost:8000/docs`

---

## API Keys Setup

### OpenAI (GPT-4 Vision API)
1. Go to: https://platform.openai.com/
2. Sign up for account
3. Navigate to API Keys
4. Create new secret key
5. Copy to `.env` file

**Costs:** ~$0.01-0.10 per drawing analysis (much cheaper!)
**Free tier:** $5 credit on signup (expires after 3 months)

**Note:** You can switch to Anthropic Claude later for higher accuracy if needed.

---

### Google Cloud Vision (Optional)
1. Go to: https://console.cloud.google.com/
2. Create new project
3. Enable Vision API
4. Create service account
5. Download JSON key
6. Set path in `.env`

**Costs:** ~$1-5 per 1000 images
**Free tier:** First 1000/month

---

### Stripe (Payment Processing)
1. Go to: https://stripe.com
2. Create account
3. Get API keys from dashboard
4. Add to `.env` file

**Costs:** 2.9% + $0.30 per transaction

---

## Dependencies

### Backend (`requirements.txt`)
```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
openai>=1.50.0
psycopg2-binary==2.9.9
sqlalchemy==2.0.25
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
pydantic==2.5.3
pydantic-settings==2.1.0
PyMuPDF==1.23.9
Pillow==10.2.0
openpyxl==3.1.2
pandas==2.1.4
numpy==1.26.3
opencv-python==4.9.0.80
pytesseract==0.3.10
ezdxf==1.1.3
boto3==1.34.34
stripe==7.11.0
celery==5.3.6
redis==5.0.1
```

### Frontend (`package.json`)
```json
{
  "dependencies": {
    "next": "14.1.0",
    "react": "18.2.0",
    "react-dom": "18.2.0",
    "axios": "1.6.5",
    "@stripe/stripe-js": "2.4.0",
    "tailwindcss": "3.4.1",
    "recharts": "2.10.4",
    "react-dropzone": "14.2.3",
    "react-hot-toast": "2.4.1",
    "zustand": "4.5.0"
  }
}
```

---

## Database Schema Setup

Run this SQL script:
```bash
psql -U postgres -d quantibot -f database_schema.sql
```

---

## Testing Setup

### Unit Tests
```bash
cd backend
pytest tests/
```

### Integration Tests
```bash
pytest tests/integration/
```

### Frontend Tests
```bash
cd frontend
npm test
```

---

## Deployment

### Docker Deployment
```bash
# Build images
docker-compose build

# Run containers
docker-compose up -d
```

### AWS Deployment
See `/deployment/aws_setup.md` for detailed guide

---

## Troubleshooting

### Issue: Database connection error
**Solution:**
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Restart if needed
sudo systemctl restart postgresql
```

### Issue: Claude API errors
**Solution:**
- Check API key is valid
- Verify account has credits
- Check rate limits

### Issue: File upload fails
**Solution:**
- Check AWS S3 credentials
- Verify bucket permissions
- Try local storage first

---

## Performance Optimization

### Backend
- Use Redis for caching
- Enable database connection pooling
- Implement request rate limiting

### Frontend
- Enable Next.js image optimization
- Use lazy loading for components
- Implement code splitting

### AI Processing
- Batch similar requests
- Cache common analyses
- Use smaller images when possible

---

## Security Checklist

- [ ] Change all default passwords
- [ ] Use strong JWT secret
- [ ] Enable HTTPS in production
- [ ] Set up CORS properly
- [ ] Implement rate limiting
- [ ] Sanitize all inputs
- [ ] Encrypt sensitive data
- [ ] Regular security audits

---

## Monitoring Setup

### Application Monitoring
```bash
# Install Sentry
pip install sentry-sdk

# Add to main.py
import sentry_sdk
sentry_sdk.init(dsn="your_sentry_dsn")
```

### Infrastructure Monitoring
- Use AWS CloudWatch
- Set up alerts for errors
- Monitor API response times
- Track database performance

---

## Backup Strategy

### Database Backups
```bash
# Daily backup script
pg_dump quantibot > backup_$(date +%Y%m%d).sql

# Restore
psql quantibot < backup_20250101.sql
```

### File Backups
- S3 versioning enabled
- 30-day retention
- Weekly full backups

---

## Support & Resources

- Documentation: `/docs`
- API Reference: `http://localhost:8000/docs`
- Issue Tracker: GitHub Issues
- Email: support@quantibot.ai

---

## Next Steps

1. ✅ Complete environment setup
2. ✅ Test with sample drawing
3. ✅ Generate first BOQ
4. 📧 Share with beta users
5. 🚀 Launch to market

---

*For detailed implementation guides, see the `/docs` folder.*
