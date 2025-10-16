# 🏠 Local Development Deployment Guide

This comprehensive guide will help you set up and run the Hacktoberfest-2025 project on your local machine for development and testing. All commands are optimized for Windows PowerShell.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [Database Setup](#database-setup)
6. [Running the Full Stack](#running-the-full-stack)
7. [Python Services](#python-services)
8. [Java Projects](#java-projects)
9. [Development Tools](#development-tools)
10. [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

### Required Software

| Software | Version | Download Link |
|----------|---------|---------------|
| **Git** | Latest | [git-scm.com](https://git-scm.com/downloads) |
| **Node.js** | v18.x or higher | [nodejs.org](https://nodejs.org/) |
| **npm** | v9.x or higher | Included with Node.js |
| **Python** | 3.8+ | [python.org](https://www.python.org/downloads/) |
| **MongoDB** | 7.x | [mongodb.com](https://www.mongodb.com/try/download/community) |

### Optional Software

| Software | Purpose | Download Link |
|----------|---------|---------------|
| **VS Code** | Recommended IDE | [code.visualstudio.com](https://code.visualstudio.com/) |
| **Postman** | API testing | [postman.com](https://www.postman.com/downloads/) |
| **MongoDB Compass** | Database GUI | [mongodb.com/products/compass](https://www.mongodb.com/products/compass) |
| **Java JDK** | For Java projects | [oracle.com/java](https://www.oracle.com/java/technologies/downloads/) |

### Verify Installation

Run these commands to verify your setup:

```powershell
# Check Git
git --version

# Check Node.js and npm
node --version
npm --version

# Check Python
python --version
pip --version

# Check MongoDB (if installed locally)
mongod --version
```

Expected output should show version numbers for each tool.

## 🚀 Initial Setup

### 1. Clone the Repository

```powershell
# Clone the repository
git clone https://github.com/hari7261/Hacktoberfest-2025.git

# Navigate to project directory
cd Hacktoberfest-2025

# Verify you're in the correct directory
pwd
```

### 2. Project Structure Overview

```
Hacktoberfest-2025/
├── backend/              # Backend services
│   ├── src/             # TypeScript source files
│   ├── app.py           # Python Flask API
│   ├── package.json     # Node.js dependencies
│   └── requirements.txt # Python dependencies
├── frontend/            # Frontend application
│   ├── components/      # React components
│   ├── pages/          # Next.js pages
│   └── package.json    # Frontend dependencies
├── docs/               # Documentation
├── python/             # Python utilities
├── java/               # Java projects
└── docker-compose.yml  # Container orchestration
```

## 🔙 Backend Setup

### Option A: Node.js/TypeScript Backend

#### 1. Install Dependencies

```powershell
# Navigate to backend directory
cd backend

# Install all npm packages
npm install

# If you encounter errors, try:
npm install --legacy-peer-deps
```

#### 2. Configure Environment Variables

Create a `.env` file in the `backend/` directory:

```powershell
# Create .env file
New-Item -Path ".env" -ItemType "file" -Force
```

Add the following configuration to `.env`:

```env
# Server Configuration
NODE_ENV=development
PORT=3001

# Database Configuration
DATABASE_URL=mongodb://localhost:27017/hacktoberfest
DB_NAME=hacktoberfest

# Authentication
JWT_SECRET=your-super-secret-jwt-key-change-in-production
JWT_EXPIRES_IN=7d

# Security
CORS_ORIGIN=http://localhost:3000
API_RATE_LIMIT=100

# Logging
LOG_LEVEL=debug
```

#### 3. Run Backend in Development Mode

```powershell
# Start development server with hot reload
npm run dev

# Alternative: Build and run production mode
npm run build
npm start
```

Backend should now be running at: `http://localhost:3001`

#### 4. Verify Backend is Running

Open a new PowerShell window:

```powershell
# Test health endpoint
Invoke-WebRequest -Uri "http://localhost:3001/health" -Method GET

# Or use curl if available
curl http://localhost:3001/health
```

Expected response: `{"status":"healthy"}`

### Option B: Python/Flask Backend

#### 1. Create Virtual Environment

```powershell
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### 2. Install Python Dependencies

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Verify installations
pip list
```

#### 3. Configure Flask Environment

Create `.env` file:

```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
FLASK_DEBUG=1

# Database
DATABASE_URL=postgresql://localhost:5432/hacktoberfest

# Security
SECRET_KEY=your-flask-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key

# Server
PORT=5000
```

#### 4. Run Flask Application

```powershell
# Run Flask development server
python app.py

# Or use Flask CLI
flask run --host=0.0.0.0 --port=5000
```

Flask app should be running at: `http://localhost:5000`

## 🎨 Frontend Setup

### 1. Install Frontend Dependencies

```powershell
# Navigate to frontend directory from root
cd frontend

# Install dependencies
npm install

# If you have package-lock conflicts
npm install --force
```

### 2. Configure Frontend Environment

Create `.env.local` file in `frontend/`:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:3001
NEXT_PUBLIC_API_TIMEOUT=30000

# Environment
NEXT_PUBLIC_ENVIRONMENT=development
NEXT_PUBLIC_APP_NAME=Hacktoberfest 2025

# Features
NEXT_PUBLIC_ENABLE_ANALYTICS=false
NEXT_PUBLIC_ENABLE_LOGGING=true
```

### 3. Run Frontend Development Server

```powershell
# Start Next.js development server
npm run dev

# Or specify custom port
npm run dev -- -p 3000
```

Frontend should now be running at: `http://localhost:3000`

### 4. Build for Production (Optional)

```powershell
# Create production build
npm run build

# Test production build locally
npm start
```

## 🗄️ Database Setup

### MongoDB Setup (for Node.js Backend)

#### Option 1: Local MongoDB Installation

```powershell
# Start MongoDB service (if installed as service)
Start-Service MongoDB

# Or run MongoDB manually
mongod --dbpath "C:\data\db"

# Create database and collections
mongosh
```

In MongoDB shell:

```javascript
// Switch to database
use hacktoberfest

// Create collections
db.createCollection('users')
db.createCollection('projects')
db.createCollection('contributions')

// Create indexes
db.users.createIndex({ email: 1 }, { unique: true })
db.projects.createIndex({ name: 1 })

// Verify
show collections
```

#### Option 2: MongoDB Atlas (Cloud)

1. Create free account at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create a cluster
3. Get connection string
4. Update `DATABASE_URL` in `.env`:

```env
DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/hacktoberfest?retryWrites=true&w=majority
```

### PostgreSQL Setup (for Python Backend)

#### Install PostgreSQL

1. Download from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run installer
3. Remember the password you set for `postgres` user

#### Create Database

```powershell
# Connect to PostgreSQL
psql -U postgres

# In psql prompt:
CREATE DATABASE hacktoberfest;
CREATE USER hackuser WITH PASSWORD 'securepassword';
GRANT ALL PRIVILEGES ON DATABASE hacktoberfest TO hackuser;
\q
```

Update `.env`:

```env
DATABASE_URL=postgresql://hackuser:securepassword@localhost:5432/hacktoberfest
```

## 🚦 Running the Full Stack

### Start All Services

Open three separate PowerShell windows:

**Window 1 - Backend:**
```powershell
cd Hacktoberfest-2025\backend
npm run dev
```

**Window 2 - Frontend:**
```powershell
cd Hacktoberfest-2025\frontend
npm run dev
```

**Window 3 - Database:**
```powershell
# MongoDB
mongod --dbpath "C:\data\db"

# Or if using service
Start-Service MongoDB
```

### Verify All Services

```powershell
# Check backend
Invoke-WebRequest -Uri "http://localhost:3001/health"

# Check frontend (open in browser)
Start-Process "http://localhost:3000"

# Check database connection
mongosh --eval "db.adminCommand('ping')"
```

## 🐍 Python Services

### Running Python Utilities

```powershell
# Activate virtual environment
cd python
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run specific scripts
python accuracy.py
python fileorganizer.py
```

### Common Python Scripts

```powershell
# File organizer
python fileorganizer.py --path "C:\Downloads" --organize

# Accuracy calculator
python accuracy.py --dataset "data.csv"

# Web scraper (if available)
python web_scraper.py --url "https://example.com"
```

## ☕ Java Projects

### Compile and Run Java Programs

```powershell
# Navigate to java directory
cd java

# Compile Java file
javac AdvancedDataStructure_AVLTree.java

# Run compiled program
java AdvancedDataStructure_AVLTree

# Compile with dependencies (if needed)
javac -cp "lib/*" YourProgram.java
```

### Using IDE (Recommended)

1. Open project in IntelliJ IDEA or Eclipse
2. Set JDK path (File → Project Structure → SDKs)
3. Build project
4. Run main class

## 🛠️ Development Tools

### Recommended VS Code Extensions

```powershell
# Install extensions via command line
code --install-extension dbaeumer.vscode-eslint
code --install-extension esbenp.prettier-vscode
code --install-extension mongodb.mongodb-vscode
code --install-extension ms-python.python
code --install-extension redhat.java
```

### Git Configuration

```powershell
# Set up Git user
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Create feature branch
git checkout -b feature/your-feature-name

# Commit changes
git add .
git commit -m "Description of changes"

# Push to remote
git push origin feature/your-feature-name
```

### Testing

```powershell
# Backend tests (Node.js)
cd backend
npm test
npm run test:watch
npm run test:coverage

# Frontend tests
cd frontend
npm test
npm run test:e2e

# Python tests
cd backend
pytest
pytest --cov=app tests/
```

## 🐛 Troubleshooting

### Common Issues and Solutions

#### Issue 1: Port Already in Use

**Problem:** `Error: listen EADDRINUSE: address already in use :::3001`

**Solution:**
```powershell
# Find process using port
Get-Process -Id (Get-NetTCPConnection -LocalPort 3001).OwningProcess

# Kill the process
Stop-Process -Id <PID> -Force

# Or change port in .env file
PORT=3002
```

#### Issue 2: Module Not Found

**Problem:** `Cannot find module 'express'`

**Solution:**
```powershell
# Clear node_modules and reinstall
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install

# Or use npm ci for clean install
npm ci
```

#### Issue 3: Python Virtual Environment Issues

**Problem:** Cannot activate virtual environment

**Solution:**
```powershell
# Enable script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Recreate virtual environment
Remove-Item -Recurse -Force venv
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### Issue 4: MongoDB Connection Failed

**Problem:** `MongooseServerSelectionError`

**Solution:**
```powershell
# Check if MongoDB is running
Get-Service MongoDB

# Start MongoDB service
Start-Service MongoDB

# Or check if mongod is running
Get-Process mongod

# Verify connection
mongosh --eval "db.adminCommand('ping')"
```

#### Issue 5: Database Authentication Failed

**Problem:** `Authentication failed`

**Solution:**
```powershell
# MongoDB - check connection string format
# Correct: mongodb://username:password@localhost:27017/dbname

# PostgreSQL - verify credentials
psql -U postgres -d hacktoberfest -c "SELECT version();"

# Reset password if needed
ALTER USER hackuser WITH PASSWORD 'newpassword';
```

#### Issue 6: CORS Errors

**Problem:** `Access-Control-Allow-Origin blocked`

**Solution:**
Update backend CORS configuration:

```javascript
// backend/src/index.ts
import cors from 'cors';

app.use(cors({
  origin: 'http://localhost:3000',
  credentials: true
}));
```

And verify `.env`:
```env
CORS_ORIGIN=http://localhost:3000
```

#### Issue 7: TypeScript Compilation Errors

**Problem:** `Cannot find name 'x'` or type errors

**Solution:**
```powershell
# Clear TypeScript cache
Remove-Item -Recurse -Force dist

# Reinstall types
npm install --save-dev @types/node @types/express

# Rebuild
npm run build
```

#### Issue 8: High CPU Usage

**Problem:** Development server consuming high CPU

**Solution:**
```powershell
# Use polling instead of file watching
npm run dev -- --poll

# Or reduce file watchers
npm run dev -- --max-old-space-size=4096
```

### Getting Additional Help

```powershell
# View npm logs
npm config get cache
type "$(npm config get cache)\_logs\*-debug.log"

# Check system resources
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10

# Network diagnostics
Test-NetConnection -ComputerName localhost -Port 3001
```

## 📊 Performance Optimization

### Development Speed Tips

1. **Use SSD** for project files
2. **Exclude node_modules** from antivirus scanning
3. **Enable WSL2** for better performance (optional)
4. **Use npm ci** instead of npm install
5. **Clear cache** regularly: `npm cache clean --force`

### Memory Management

```powershell
# Increase Node.js memory limit
$env:NODE_OPTIONS="--max-old-space-size=4096"

# Run with increased memory
node --max-old-space-size=4096 dist/index.js
```

## 📝 Development Workflow

### Daily Development Routine

```powershell
# 1. Update codebase
git pull origin main

# 2. Install any new dependencies
npm install

# 3. Start services
# Terminal 1: Backend
cd backend; npm run dev

# Terminal 2: Frontend  
cd frontend; npm run dev

# 4. Make changes and test

# 5. Run tests before committing
npm test

# 6. Commit and push
git add .
git commit -m "Your message"
git push
```

## 🔐 Security Considerations

### Development Security

- ✅ Never commit `.env` files
- ✅ Use different secrets for dev/prod
- ✅ Keep dependencies updated: `npm audit fix`
- ✅ Use HTTPS in local development (optional)
- ✅ Implement rate limiting
- ✅ Validate all inputs

### Check for Vulnerabilities

```powershell
# Check npm packages
npm audit
npm audit fix

# Check Python packages
pip-audit
safety check
```

## 📚 Additional Resources

- [Node.js Documentation](https://nodejs.org/docs/)
- [Next.js Documentation](https://nextjs.org/docs)
- [MongoDB Manual](https://docs.mongodb.com/manual/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [PowerShell Documentation](https://docs.microsoft.com/powershell/)

## 🆘 Need Help?

1. Check the [main deployment README](./README.md)
2. Search [existing issues](https://github.com/hari7261/Hacktoberfest-2025/issues)
3. Ask in discussions
4. Open a new issue with:
   - Steps to reproduce
   - Error messages
   - System information
   - Screenshots

---

**Happy Coding! 🚀**

Last Updated: October 2025
