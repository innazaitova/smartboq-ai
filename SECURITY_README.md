# ⚠️ SECURITY WARNING - DO NOT COMMIT ACTUAL .ENV FILE

This project contains sensitive information in `.env` files.

## Before Pushing to GitHub:

1. ✅ Verify `.gitignore` excludes `.env` files
2. ✅ Use `env.example` files as templates (already included)
3. ⚠️ **NEVER** commit files containing:
   - API keys (OpenAI, AWS, etc.)
   - Database passwords
   - JWT secrets
   - Any production credentials

## What's Included:

- ✅ `.gitignore` - Protects sensitive files
- ✅ `backend/env.example` - Template for backend config
- ✅ `frontend/.env.example` - Template for frontend config
- ✅ All hardcoded URLs replaced with environment variables
- ✅ CORS configured for production domains

## Next Steps:

1. **Generate Secure JWT Secret:**
   ```bash
   # Python
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Update Production .env files:**
   - Copy `env.example` to `.env`
   - Replace placeholder values with real credentials
   - Never commit `.env` files

3. **Deploy:**
   - Frontend: Vercel (see `PRODUCTION_DEPLOY.md`)
   - Backend: Railway/Render (see `PRODUCTION_DEPLOY.md`)

## Security Checklist Before Deploy:

- [ ] Changed JWT_SECRET_KEY from default
- [ ] Updated OPENAI_API_KEY with valid key
- [ ] Set strong DATABASE_PASSWORD
- [ ] Configured ALLOWED_ORIGINS for production domain
- [ ] Verified `.gitignore` excludes `.env`
- [ ] Removed any test/debug code
- [ ] Database uses SSL in production

## Current Status:
✅ Code is production-ready
✅ Security configurations in place
⚠️ Update environment variables before deployment
