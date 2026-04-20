---
description: Deploy TechnoPath to GitHub
---

# Deploy TechnoPath to GitHub

## Prerequisites
- Git installed on your system
- GitHub account
- Personal Access Token (classic) with repo scope

## Steps

### 1. Initialize Git Repository (if not already done)
// turbo
```bash
git init
```

### 2. Add all files to staging
// turbo
```bash
git add .
```

### 3. Create initial commit
// turbo
```bash
git commit -m "Initial commit: TechnoPath Campus Guide System"
```

### 4. Create GitHub Repository
1. Go to https://github.com/new
2. Repository name: `technopath` (or your preferred name)
3. Set to Public or Private
4. **Do NOT initialize with README** (we already have one)
5. Click "Create repository"

### 5. Link Local Repository to GitHub
Replace `YOUR_USERNAME` with your GitHub username:

**For HTTPS:**
```bash
git remote add origin https://github.com/YOUR_USERNAME/technopath.git
```

**For SSH:**
```bash
git remote add origin git@github.com:YOUR_USERNAME/technopath.git
```

### 6. Push to GitHub
// turbo
```bash
git branch -M main
git push -u origin main
```

## Optional: Add .gitignore

Before committing, ensure `.gitignore` includes:

```
# Dependencies
node_modules/
.venv/
venv/

# Build outputs
dist/
build/

# Environment files
.env
.env.local
.env.*.local

# IDE
.idea/
.vscode/
.aider*

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Database
*.db
*.sqlite3

# Logs
*.log

# OS
.DS_Store
Thumbs.db
```

## Troubleshooting

**If push fails due to large files:**
```bash
# Remove large files from git history
git rm --cached cleanup_unused.ps1
git commit -m "Remove large script file"
git push
```

**If authentication fails:**
- Use Personal Access Token instead of password
- Or set up SSH keys: https://docs.github.com/en/authentication/connecting-to-github-with-ssh

## Verification
After pushing, visit:
`https://github.com/YOUR_USERNAME/technopath`

To verify all files are uploaded.
