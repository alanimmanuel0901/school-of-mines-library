# 🐍 Python 3.14 Fix - Quick Reference

## Problem
**psycopg2-binary doesn't work with Python 3.14 on Render**

## Solution
**Use modern psycopg[binary] driver**

---

## ✅ What Changed

### requirements.txt
```diff
- psycopg2-binary==2.9.9
+ psycopg[binary]==3.1.18
```

---

## 🚀 Deploy to Render

### 1. Push Changes
```bash
git add .
git commit -m "Fix Python 3.14 compatibility - use psycopg3"
git push origin main
```

### 2. Create Render Service
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

### 3. Add PostgreSQL
- Create database on Render
- Copy Internal Database URL

### 4. Set Environment Variable
- **Key:** `DATABASE_URL`
- **Value:** Your PostgreSQL URL

### 5. Deploy!
App will use psycopg3 (Python 3.14 compatible)

---

## 🔧 Local Testing

### Run with SQLite
```bash
python app.py
```

### Test with PostgreSQL
```bash
export DATABASE_URL="postgresql://..."
python app.py
```

---

## ✅ Verification Checklist

- [x] requirements.txt has `psycopg[binary]==3.1.18`
- [x] No `psycopg2-binary` in dependencies
- [x] Flask app runs locally with SQLite
- [ ] Deployed to Render successfully
- [ ] Works with PostgreSQL on production

---

## 📋 Requirements

**Complete requirements.txt:**
```txt
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Werkzeug==3.0.1
requests==2.31.0
gunicorn==21.2.0
psycopg[binary]==3.1.18
```

---

## 💡 Key Points

✅ **No code changes needed** - Flask-SQLAlchemy handles everything  
✅ **SQLite still works** - For local development  
✅ **PostgreSQL ready** - For production on Render  
✅ **Python 3.14 compatible** - Modern driver  

---

## 🎯 Status

**Before:** ❌ psycopg2-binary (incompatible with Python 3.14)  
**After:** ✅ psycopg[binary] (fully compatible)  

---

**Quick Start:** Just push and deploy! 🚀
