# QuantiBot AI - Deployment Guide

## Prerequisites

- Docker and Docker Compose installed
- Domain name configured (for production)
- SSL certificates (Let's Encrypt recommended)
- Cloud provider account (AWS, DigitalOcean, etc.)

## Quick Start with Docker

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/quantibot-ai.git
cd quantibot-ai
```

### 2. Configure Environment
```bash
# Copy example environment file
cp backend/.env.example backend/.env

# Edit with your actual values
nano backend/.env
```

**Required Configuration:**
- `ANTHROPIC_API_KEY` - Get from https://console.anthropic.com
- `JWT_SECRET_KEY` - Generate with: `openssl rand -hex 32`
- `DATABASE_URL` - PostgreSQL connection string
- `AWS_ACCESS_KEY_ID` & `AWS_SECRET_ACCESS_KEY` - AWS credentials
- `STRIPE_SECRET_KEY` - Get from https://dashboard.stripe.com

### 3. Start Services
```bash
# Build and start all containers
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend
```

### 4. Initialize Database
```bash
# Run database migrations
docker-compose exec backend python -c "
from database import engine
from sqlalchemy import text

with open('database_schema.sql', 'r') as f:
    engine.execute(text(f.read()))
"
```

### 5. Access Application
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

## Production Deployment

### Option 1: AWS Deployment

#### Step 1: Set up RDS (PostgreSQL)
```bash
aws rds create-db-instance \
  --db-instance-identifier quantibot-db \
  --db-instance-class db.t3.medium \
  --engine postgres \
  --master-username admin \
  --master-user-password YOUR_PASSWORD \
  --allocated-storage 50
```

#### Step 2: Set up S3 Bucket
```bash
aws s3 mb s3://quantibot-drawings
aws s3api put-bucket-cors --bucket quantibot-drawings --cors-configuration file://cors.json
```

**cors.json:**
```json
{
  "CORSRules": [
    {
      "AllowedOrigins": ["*"],
      "AllowedMethods": ["GET", "POST", "PUT", "DELETE"],
      "AllowedHeaders": ["*"]
    }
  ]
}
```

#### Step 3: Deploy with ECS Fargate
```bash
# Build and push images
docker build -t quantibot-backend ./backend
docker tag quantibot-backend:latest YOUR_ECR_REPO/quantibot-backend:latest
docker push YOUR_ECR_REPO/quantibot-backend:latest

docker build -t quantibot-frontend ./frontend
docker tag quantibot-frontend:latest YOUR_ECR_REPO/quantibot-frontend:latest
docker push YOUR_ECR_REPO/quantibot-frontend:latest

# Create ECS service
aws ecs create-service \
  --cluster quantibot \
  --service-name quantibot-backend \
  --task-definition quantibot-backend \
  --desired-count 2 \
  --launch-type FARGATE
```

### Option 2: DigitalOcean Deployment

#### Step 1: Create Droplet
```bash
# Create droplet with Docker
doctl compute droplet create quantibot \
  --image docker-20-04 \
  --size s-2vcpu-4gb \
  --region nyc1
```

#### Step 2: Set up Database
```bash
# Create managed PostgreSQL database
doctl databases create quantibot-db \
  --engine pg \
  --region nyc1 \
  --size db-s-2vcpu-4gb
```

#### Step 3: Deploy Application
```bash
# SSH into droplet
ssh root@YOUR_DROPLET_IP

# Clone repository
git clone https://github.com/yourusername/quantibot-ai.git
cd quantibot-ai

# Configure environment
cp backend/.env.example backend/.env
nano backend/.env

# Start services
docker-compose up -d
```

### Option 3: Vercel (Frontend) + Railway (Backend)

#### Deploy Frontend to Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel --prod
```

#### Deploy Backend to Railway
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login and deploy
railway login
railway up
```

## SSL/HTTPS Configuration

### Using Let's Encrypt with Nginx

**nginx/nginx.conf:**
```nginx
server {
    listen 80;
    server_name quantibot.ai www.quantibot.ai;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name quantibot.ai www.quantibot.ai;

    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;

    # Frontend
    location / {
        proxy_pass http://frontend:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Backend API
    location /api/ {
        proxy_pass http://backend:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Generate SSL Certificates
```bash
# Install certbot
apt-get install certbot python3-certbot-nginx

# Generate certificate
certbot --nginx -d quantibot.ai -d www.quantibot.ai

# Auto-renewal
certbot renew --dry-run
```

## Monitoring & Logging

### Set up Logging
```bash
# Create log directory
mkdir -p logs

# Configure log rotation
cat > /etc/logrotate.d/quantibot << EOF
/app/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 root root
}
EOF
```

### Set up Monitoring (Prometheus + Grafana)

**docker-compose.monitoring.yml:**
```yaml
services:
  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus_data:/prometheus
    ports:
      - "9090:9090"

  grafana:
    image: grafana/grafana
    ports:
      - "3001:3000"
    volumes:
      - grafana_data:/var/lib/grafana
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

volumes:
  prometheus_data:
  grafana_data:
```

Start monitoring:
```bash
docker-compose -f docker-compose.monitoring.yml up -d
```

## Backup & Recovery

### Database Backup
```bash
# Automated daily backup
cat > /etc/cron.daily/backup-db << 'EOF'
#!/bin/bash
BACKUP_DIR="/backups/postgres"
DATE=$(date +%Y%m%d_%H%M%S)

docker-compose exec -T db pg_dump -U postgres quantibot > \
  $BACKUP_DIR/quantibot_$DATE.sql

# Keep only last 30 days
find $BACKUP_DIR -name "quantibot_*.sql" -mtime +30 -delete
EOF

chmod +x /etc/cron.daily/backup-db
```

### Database Restore
```bash
# Restore from backup
docker-compose exec -T db psql -U postgres quantibot < \
  /backups/postgres/quantibot_20250101_120000.sql
```

## Performance Optimization

### Enable Caching
```python
# Add Redis caching to backend
from redis import Redis
from functools import lru_cache

redis_client = Redis.from_url(os.getenv('REDIS_URL'))

@lru_cache(maxsize=1000)
def get_unit_rates(region: str):
    # Cache frequently accessed data
    pass
```

### Scale Services
```bash
# Scale backend workers
docker-compose up -d --scale worker=3

# For AWS ECS
aws ecs update-service \
  --cluster quantibot \
  --service quantibot-backend \
  --desired-count 5
```

## Health Checks

### Backend Health Endpoint
Access: http://localhost:8000/health

Response:
```json
{
  "status": "healthy",
  "database": "connected",
  "redis": "connected",
  "version": "1.0.0"
}
```

### Monitoring Script
```bash
#!/bin/bash
# check-health.sh

BACKEND_URL="http://localhost:8000/health"
FRONTEND_URL="http://localhost:3000"

# Check backend
if ! curl -f $BACKEND_URL > /dev/null 2>&1; then
  echo "Backend is down! Restarting..."
  docker-compose restart backend
fi

# Check frontend
if ! curl -f $FRONTEND_URL > /dev/null 2>&1; then
  echo "Frontend is down! Restarting..."
  docker-compose restart frontend
fi
```

Add to crontab:
```bash
*/5 * * * * /path/to/check-health.sh
```

## Troubleshooting

### Common Issues

**Issue: Database connection error**
```bash
# Check database is running
docker-compose ps db

# Check connection string
docker-compose exec backend python -c "
from database import engine
print(engine.url)
"

# Test connection
docker-compose exec db psql -U postgres -c "SELECT 1"
```

**Issue: File upload failures**
```bash
# Check S3 credentials
aws s3 ls s3://quantibot-drawings

# Check permissions
aws s3api get-bucket-policy --bucket quantibot-drawings

# Test upload
aws s3 cp test.pdf s3://quantibot-drawings/test.pdf
```

**Issue: Slow AI processing**
```bash
# Check Anthropic API rate limits
# Upgrade plan or implement queuing

# Monitor processing times
docker-compose logs -f backend | grep "Processing time"
```

## Security Checklist

- [ ] Change all default passwords
- [ ] Enable SSL/HTTPS
- [ ] Set up firewall rules
- [ ] Configure CORS properly
- [ ] Enable rate limiting
- [ ] Set up automated backups
- [ ] Configure log rotation
- [ ] Enable security headers
- [ ] Set up monitoring alerts
- [ ] Regular security updates

## Support

For deployment issues:
- Email: support@quantibot.ai
- Docs: https://docs.quantibot.ai
- GitHub Issues: https://github.com/yourusername/quantibot-ai/issues
