# QuantiBot AI - Production Deployment Guide

## 🚀 Quick Deploy

### Frontend (Vercel)
1. Push to GitHub
2. Import project in Vercel
3. Set environment variable: `NEXT_PUBLIC_API_URL` = your backend URL
4. Deploy

### Backend (Render)
1. Create PostgreSQL database on Render
2. Create Web Service on Render
3. Set all environment variables from `backend/env.example`
4. Deploy FastAPI app
5. Run database initialization

## 📋 Pre-Deployment Checklist

### Security
- [x] .gitignore created (excludes .env files)
- [x] Environment variables configured
- [x] CORS configured for production domains
- [x] JWT_SECRET_KEY changed to secure random string
- [ ] Database password is strong
- [ ] OpenAI API key is valid

### Configuration
- [x] Hardcoded URLs removed from code
- [x] Environment-based configuration
- [ ] Production database URL configured
- [ ] SMTP email configured (optional)
- [ ] AWS S3 configured for file storage (optional)

## 🔧 Environment Variables

### Frontend (Vercel)
```bash
NEXT_PUBLIC_API_URL=https://your-app-name.onrender.com
```

### Backend (Render)
```bash
DATABASE_URL=postgresql://user:pass@host/quantibot
OPENAI_API_KEY=sk-your-real-key
JWT_SECRET_KEY=your-secure-random-32-char-string
ALLOWED_ORIGINS=https://your-frontend.vercel.app
ENVIRONMENT=production
```

## 📝 Deployment Steps

### 1. Prepare Repository
```bash
# Add and commit production files
git add .
git commit -m "Production ready: Secure configuration"
git push origin main
```

### 2. Deploy Database (Render)
1. Go to https://render.com → New → PostgreSQL
2. Choose a name: `quantibot-db`
3. Database: `quantibot`
4. User: `quantibot_user`
5. Region: Choose closest to your users
6. Plan: **Free** (for testing) or **Starter $7/month**
7. Click **Create Database**
8. Copy the **External Database URL** (starts with `postgresql://`)
9. Wait for database to provision (~2 minutes)

### 3. Initialize Database Schema
```bash
# Connect to your Render database and run schema
psql "your-render-database-url-here" -f backend/database_schema.sql
```

**Or via Render Dashboard:**
1. Go to your database → Connect → Web Shell
2. Paste contents of `backend/database_schema.sql`
3. Execute

### 4. Deploy Backend (Render)
1. Go to https://render.com → New → Web Service
2. Connect your GitHub repository
3. **Settings:**
   - **Name**: `quantibot-api` (or your app name)
   - **Root Directory**: `backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: **Free** (spins down after inactivity) or **Starter $7/month** (always on)

4. **Environment Variables** (Add in Render dashboard):
```bash
DATABASE_URL=postgresql://...  # From step 2
OPENAI_API_KEY=sk-...
JWT_SECRET_KEY=your-generated-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
ALLOWED_ORIGINS=https://your-frontend.vercel.app
ENVIRONMENT=production
```

5. Click **Create Web Service**
6. Wait for deployment (~3-5 minutes)
7. Copy your service URL: `https://your-app-name.onrender.com`

### 5. Deploy Frontend (Vercel)
1. Go to https://vercel.com → Add New → Project
2. Import from GitHub
3. **Settings:**
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (auto-detected)
   - **Output Directory**: `.next` (auto-detected)

4. **Environment Variables**:
   - Key: `NEXT_PUBLIC_API_URL`
   - Value: `https://your-app-name.onrender.com` (from step 4)

5. Click **Deploy**
6. Wait for deployment (~2 minutes)
7. Your app is live at: `https://your-project.vercel.app`

### 6. Update CORS
1. Go back to Render dashboard → Your backend service
2. Update environment variable:
   - `ALLOWED_ORIGINS` = `https://your-project.vercel.app`
3. Service will auto-redeploy

## 🔍 Post-Deployment Verification

1. ✅ Frontend loads: `https://your-project.vercel.app`
2. ✅ API responds: `https://your-app.onrender.com/health`
3. ✅ User registration works
4. ✅ User login works
5. ✅ Project creation works
6. ✅ File upload works
7. ✅ No CORS errors in browser console

## 💰 Cost Estimate

### Option 1: Free Tier (Testing)
- **Vercel Frontend**: Free
- **Render Backend**: Free (spins down after 15 min inactivity)
- **Render PostgreSQL**: Free (90 days, then $7/month)
- **OpenAI API**: Pay per use (~$0.01-0.10 per drawing)
- **Total**: ~$0/month + AI costs (backend may be slow on free tier)

### Option 2: Production (Recommended)
- **Vercel Frontend**: Free (Hobby) or $20/month (Pro)
- **Render Backend**: $7/month (Starter - always on, faster)
- **Render PostgreSQL**: $7/month (Starter - 1GB RAM, 10GB storage)
- **OpenAI API**: ~$0.01-0.10 per drawing analysis
- **Total**: **$14/month** + AI usage costs

## 🐛 Troubleshooting

### Backend won't start
- Check Render logs: Dashboard → Service → Logs
- Verify Python version (3.12 required)
- Check `requirements.txt` format
- Ensure `DATABASE_URL` is correct

### Database connection failed
- Verify DATABASE_URL format: `postgresql://user:pass@host/dbname`
- Check database is in same region as backend
- Ensure database is not paused (free tier)
- Test connection in Render web shell

### Frontend can't connect to backend
- Verify `NEXT_PUBLIC_API_URL` in Vercel
- Check CORS: `ALLOWED_ORIGINS` must include Vercel URL
- Test backend directly: `https://your-app.onrender.com/health`
- Check browser console for errors

### Render Free Tier Limitations
- Backend spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- Database limited to 1GB (free tier)
- **Solution**: Upgrade to Starter plan ($7/month) for always-on service

### OpenAI API Errors
- Verify API key is valid: https://platform.openai.com/api-keys
- Check billing is set up: https://platform.openai.com/account/billing
- Monitor usage: https://platform.openai.com/usage
- Rate limits: https://platform.openai.com/account/limits

## 📊 Monitoring (Optional)

### Render Built-in Monitoring
- CPU/Memory usage in dashboard
- Logs in real-time
- Automatic health checks

### Additional Tools
- **Sentry**: Error tracking (add to backend)
- **LogTail**: Advanced log management
- **Uptime Robot**: Ping backend every 5 min (keeps free tier alive!)

## 🔐 Security Best Practices

1. **Rotate secrets regularly** (JWT, API keys)
2. **Enable 2FA** on Vercel and Render accounts
3. **Use environment variables** for all secrets
4. **Monitor API usage** to detect abuse
5. **Set up rate limiting** (optional)
6. **Regular backups** of PostgreSQL database

## 📞 Support

### Render Issues
- Dashboard: https://dashboard.render.com
- Docs: https://render.com/docs
- Status: https://status.render.com

### Vercel Issues  
- Dashboard: https://vercel.com/dashboard
- Docs: https://vercel.com/docs
- Status: https://vercel-status.com

---

🎉 **Congratulations!** Your AI-powered construction QS platform is now live!
