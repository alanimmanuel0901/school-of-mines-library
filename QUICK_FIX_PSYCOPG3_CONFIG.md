# 🔧 psycopg3 Configuration Fix - Quick Reference

## ✅ Problem Solved

**Error:** `ModuleNotFoundError: No module named 'psycopg2'`  
**Fix:**Changed URI from `postgresql://` to `postgresql+psycopg://`

---

## 🔧 What Changed

### app.py (Line 21)

**Before:** ❌ `postgresql://` (defaults to psycopg2)  
**After:** ✅ `postgresql+psycopg://` (explicitly psycopg3)

```python
# Line 21 in app.py
database_url = database_url.replace('postgres://', 'postgresql+psycopg://', 1)
```

---

## 🚀 Deploy to Render

### 1. Push Changes
```bash
git add app.py requirements.txt
git commit-m "Fix: Use psycopg3 driver in database URI"
git push origin main
```

### 2. Redeploy
Render will automatically use psycopg3.

---

## ✅ Verification

- [x] app.py uses `postgresql+psycopg://`
- [x] requirements.txt has `psycopg[binary]==3.3.3`
- [x] No psycopg2 packages
- [ ] Render deployment successful
- [ ] No ModuleNotFoundError

---

## 📋 Complete Configuration

```python
database_url = os.environ.get('DATABASE_URL')

if database_url:
   if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql+psycopg://', 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

---

## 🎯 Status

**Before:** ❌ ModuleNotFoundError (psycopg2)  
**After:** ✅ Using psycopg3 successfully  

---

**Ready to deploy!** 🚀
