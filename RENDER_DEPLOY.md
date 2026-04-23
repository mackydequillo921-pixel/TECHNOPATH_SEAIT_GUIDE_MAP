# Deploy TechnoPath to Render (100% Complete System)

This guide deploys both Frontend (Vue.js) and Backend (Django) to Render.com

## Quick Deploy (Using Render Blueprint)

### 1. Push Code to GitHub
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Deploy on Render
1. Go to [dashboard.render.com](https://dashboard.render.com)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repo: `mackydequillo921-pixel/TECHNOPATH_SEAIT_GUIDE_MAP`
4. Click **"Apply"** - Render will automatically create:
   - ✅ Frontend (Static Site)
   - ✅ Backend (Web Service with persistent SQLite)

### 3. Set Environment Variables (if needed)
After deployment, go to Backend service → Environment:

| Variable | Value |
|----------|-------|
| `SECRET_KEY` | (auto-generated) |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `.onrender.com,technopath-backend.onrender.com` |
| `CORS_ALLOWED_ORIGINS` | `https://technopath-frontend.onrender.com` |

### 4. URLs After Deployment
- **Frontend**: `https://technopath-frontend.onrender.com`
- **Backend API**: `https://technopath-backend.onrender.com/api`

---

## Manual Deploy (Alternative)

### Backend (Web Service)
1. Create **New Web Service**
2. Select your repo
3. Settings:
   - **Root Directory**: `backend_django`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `bash render_start.sh`
   - **Disk**: Mount at `/data` (1GB)

### Frontend (Static Site)
1. Create **New Static Site**
2. Select your repo
3. Settings:
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`

---

## Features

✅ **Frontend**: Vue.js 3 + Vite + PWA  
✅ **Backend**: Django REST API + JWT Auth  
✅ **Database**: SQLite with persistent disk  
✅ **CORS**: Configured for Render domains  
✅ **Static Files**: Auto-collected on deploy  
✅ **Media Uploads**: Supported with persistent storage  

---

## Troubleshooting

### Database not persisting?
- Ensure disk is mounted at `/data`
- Check `DATABASE_URL` is set to `sqlite:///data/technopath.db`

### CORS errors?
- Update `CORS_ALLOWED_ORIGINS` with your actual frontend URL

### Static files 404?
- Run `python manage.py collectstatic` in the start script (already included)

---

## Architecture

```
┌─────────────────────────────────────────┐
│           Render.com                    │
│  ┌─────────────┐    ┌──────────────┐   │
│  │   Frontend  │────│   Backend    │   │
│  │  (Vue.js)   │    │  (Django)    │   │
│  │   Static    │    │   Web Svc    │   │
│  │    Site     │    │              │   │
│  └─────────────┘    └──────┬───────┘   │
│                            │           │
│                     ┌──────┴──────┐   │
│                     │  SQLite DB  │   │
│                     │ /data/*.db   │   │
│                     └─────────────┘   │
└─────────────────────────────────────────┘
```
