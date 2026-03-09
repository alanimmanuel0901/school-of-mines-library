# 🚀 Quick Deploy to Render - PostgreSQL Setup

## 5-Minute Deployment Guide

### Prerequisites
- GitHub account with code pushed
- Render account (free at https://render.com)

---

## Step 1: Create Web Service

1. Login to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repo
4. Configure:

```
Name: library-system
Region: Choose yours
Branch: main
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

5. Click **"Create Web Service"**

---

## Step 2: Add PostgreSQL Database

1. In Render, click **"New +"** → **"PostgreSQL"**
2. Configure:

```
Name: library-db
Database: library_db
User: postgres
Password: (auto-generated)
```

3. Click **"Create Database"**
4. Wait ~2 minutes for provisioning

---

## Step 3: Get DATABASE_URL

1. Go to your new database dashboard
2. Find **"Internal Database URL"**
3. Copy it (looks like):
   ```
   postgresql://user:pass@host:5432/dbname
   ```

---

## Step 4: Add Environment Variable

1. Go back to your **Web Service**
2. Click **"Environment"** tab
3. Click **"Add Environment Variable"**
4. Add:

```
Key: DATABASE_URL
Value: (paste the URL from Step 3)
```

5. Click **"Save Changes"**

---

## Step 5: Deploy!

1. Go to **"Manual Deploy"** or wait for auto-deploy
2. Watch logs in **"Logs"** tab
3. Wait ~3-5 minutes
4. Your app is LIVE! 🎉

---

## ✅ Verify Deployment

### Check These:
- [ ] Website loads
- [ ] Can login as admin
- [ ] Can add books
- [ ] Can register students
- [ ] Data persists after page refresh

---

## 🔧 Local Development

### Run Locally (SQLite)
```bash
python app.py
```

No setup needed! Uses `library.db` automatically.

---

## 📊 What Changed?

### app.py (Lines 12-20)
```python
# Auto-detects environment
database_url = os.environ.get('DATABASE_URL')

if database_url:
    # Production: PostgreSQL
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    # Local: SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
```

### requirements.txt
Added:
```txt
psycopg2-binary==2.9.9
gunicorn==21.2.0
```

---

## ⚠️ Common Issues

### Issue: "DATABASE_URL not found"
**Fix:** Make sure you saved it in Environment tab

### Issue: "Module psycopg2 not found"
**Fix:** 
```bash
pip install -r requirements.txt
```

### Issue: App won't start
**Check:**
- Build logs for errors
- requirements.txt has all dependencies
- Start command is `gunicorn app:app`

---

## 💰 Render Free Tier Limits

- **Web Service:** 750 hours/month (free)
- **PostgreSQL:** 90 days free, then $7/month
- **Bandwidth:** 100GB/month
- **Storage:** 1GB for database

---

## 🎯 Quick Commands

### Local Testing
```bash
# Run Flask dev server
python app.py

# Or with gunicorn (production-like)
gunicorn app:app
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 📞 Support Links

- [Render Docs - Flask](https://render.com/docs/deploy-flask)
- [Render Docs - PostgreSQL](https://render.com/docs/databases)
- [Render Community](https://community.render.com/)

---

## ✨ Success Checklist

Before going live:

- [ ] Code pushed to GitHub
- [ ] Web Service created
- [ ] PostgreSQL database created
- [ ] DATABASE_URL added to environment
- [ ] Deployment successful
- [ ] All features tested
- [ ] Admin user created
- [ ] Sample data added

---

**🎉 You're Done! Your app is production-ready!**

---

**Quick Reference:**
- **Local:** SQLite (automatic)
- **Production:** PostgreSQL (via DATABASE_URL)
- **Server:** Gunicorn
- **Platform:** Render
- **Status:** Ready to deploy ✅
