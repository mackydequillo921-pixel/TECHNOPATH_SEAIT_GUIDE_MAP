---
description: Deploy TechnoPath to Render
---

# Deploy TechnoPath to Render

## Prerequisites
- GitHub repository already created and public
- Render account (free tier available)
- OpenAI API key (optional, for AI chatbot)

## Architecture
You'll deploy 3 services on Render:
1. **Frontend** - Static site (Vite build)
2. **Backend** - Django Web Service
3. **Chatbot** - Flask Web Service

---

## Step 1: Prepare Repository

### Add render.yaml Blueprint

Create `render.yaml` in your repo root:

```yaml
services:
  # Django Backend API
  - type: web
    name: technopath-backend
    runtime: python
    buildCommand: |
      cd backend_django && 
      pip install -r requirements.txt && 
      python manage.py collectstatic --noinput &&
      python manage.py migrate
    startCommand: cd backend_django && gunicorn technopath.wsgi:application
    envVars:
      - key: DJANGO_SECRET_KEY
        generateValue: true
      - key: DJANGO_DEBUG
        value: "False"
      - key: DATABASE_URL
        fromDatabase:
          name: technopath-db
          property: connectionString
      - key: ALLOWED_HOSTS
        value: "*"
      - key: CORS_ALLOWED_ORIGINS
        value: "https://technopath-frontend.onrender.com"
    disk:
      name: django-static
      mountPath: /app/backend_django/staticfiles
      sizeGB: 1

  # Flask Chatbot Service
  - type: web
    name: technopath-chatbot
    runtime: python
    buildCommand: cd chatbot_flask && pip install -r requirements.txt
    startCommand: cd chatbot_flask && gunicorn app:app
    envVars:
      - key: OPENAI_API_KEY
        value: ""  # Optional - set in Render dashboard
    disk:
      name: chatbot-db
      mountPath: /app/chatbot_flask
      sizeGB: 1

  # Frontend Static Site
  - type: static
    name: technopath-frontend
    runtime: node
    buildCommand: cd frontend && npm install && npm run build
    staticPublishPath: ./frontend/dist
    envVars:
      - key: VITE_API_BASE_URL
        value: "https://technopath-backend.onrender.com/api"
      - key: VITE_CHATBOT_URL
        value: "https://technopath-chatbot.onrender.com"

databases:
  - name: technopath-db
    databaseName: technopath
    user: technopath
    plan: free
```

---

## Step 2: Create Requirements Files

### backend_django/requirements.txt

```
Django>=4.2,<5.0
djangorestframework>=3.14.0
django-cors-headers>=4.0.0
dj-database-url>=2.0.0
psycopg2-binary>=2.9.0
gunicorn>=21.0.0
python-dotenv>=1.0.0
Pillow>=10.0.0
```

### chatbot_flask/requirements.txt

```
Flask>=2.3.0
flask-cors>=4.0.0
flask-limiter>=3.5.0
gunicorn>=21.0.0
python-dotenv>=1.0.0
openai>=1.0.0  # Optional
```

---

## Step 3: Configure Frontend for Production

### frontend/.env.production

```
VITE_API_BASE_URL=https://technopath-backend.onrender.com/api
VITE_CHATBOT_URL=https://technopath-chatbot.onrender.com
```

---

## Step 4: Update Django Settings

### backend_django/technopath/settings.py

Add at top:
```python
import dj_database_url
```

Replace DATABASES section:
```python
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3'),
        conn_max_age=600
    )
}
```

Update ALLOWED_HOSTS:
```python
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')
```

---

## Step 5: Deploy on Render

1. Go to https://dashboard.render.com
2. Click **New +** → **Blueprint**
3. Connect your GitHub repo
4. Select the `render.yaml` blueprint
5. Click **Apply**

Render will automatically:
- Create PostgreSQL database
- Deploy all 3 services
- Set up environment variables

---

## Step 6: Set Secrets (Important!)

After deployment, add these in Render Dashboard:

### technopath-backend service:
- `DJANGO_SECRET_KEY` - Generate at https://djecrety.ir/

### technopath-chatbot service (optional):
- `OPENAI_API_KEY` - Get from https://platform.openai.com

---

## Step 7: Update Frontend API URLs

After deployment, get your actual Render URLs and update:
- `VITE_API_BASE_URL` in frontend settings
- `VITE_CHATBOT_URL` in frontend settings

---

## Troubleshooting

**Build fails?**
- Check requirements.txt is committed
- Check render.yaml syntax

**Database connection fails?**
- Wait for database to be ready (green status)
- Check DATABASE_URL environment variable

**CORS errors?**
- Update CORS_ALLOWED_ORIGINS with actual frontend URL

**Chatbot not responding?**
- Check chatbot service is running (green status)
- Verify VITE_CHATBOT_URL matches actual URL

---

## URLs After Deployment

- **Frontend:** `https://technopath-frontend.onrender.com`
- **Backend API:** `https://technopath-backend.onrender.com/api`
- **Chatbot:** `https://technopath-chatbot.onrender.com`

---

## Free Tier Limits

- 750 hours/month (enough for 3 services running 24/7)
- 1 GB PostgreSQL storage
- Services spin down after 15 min idle (cold start delay)
