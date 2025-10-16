# 🚀 Quick Reference - Deployment Commands

Quick copy-paste commands for deploying Hacktoberfest-2025 across different environments.

## 📦 Local Development

### Start Backend (Node.js)
```powershell
cd backend
npm install
npm run dev
```

### Start Backend (Python)
```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

### Start Frontend
```powershell
cd frontend
npm install
npm run dev
```

### Start MongoDB
```powershell
Start-Service MongoDB
# Or
mongod --dbpath "C:\data\db"
```

## 🐳 Docker Deployment

### Quick Start
```powershell
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop all services
docker compose down
```

### Build and Deploy
```powershell
# Build images
docker compose build

# Start with fresh build
docker compose up --build -d

# View status
docker compose ps
```

### Individual Services
```powershell
# Start specific service
docker compose up -d backend

# Restart service
docker compose restart backend

# View logs
docker compose logs -f backend
```

## ☁️ AWS Deployment

### ECR Push
```powershell
# Login
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

# Tag and push
docker tag hacktoberfest-backend:latest ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/hacktoberfest-backend:latest
docker push ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/hacktoberfest-backend:latest
```

### ECS Deploy
```powershell
# Update service
aws ecs update-service --cluster hacktoberfest-cluster --service backend-service --force-new-deployment

# View logs
aws logs tail /ecs/hacktoberfest --follow
```

### App Runner Deploy
```powershell
aws apprunner start-deployment --service-arn SERVICE_ARN
```

## ☁️ Google Cloud Deployment

### Cloud Run Deploy
```powershell
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/hacktoberfest-backend
gcloud run deploy hacktoberfest-backend --image gcr.io/PROJECT_ID/hacktoberfest-backend --platform managed --region us-central1 --allow-unauthenticated

# View logs
gcloud logging read "resource.type=cloud_run_revision" --limit 50
```

### GKE Deploy
```powershell
# Get credentials
gcloud container clusters get-credentials hacktoberfest-cluster

# Deploy
kubectl apply -f k8s/

# View status
kubectl get pods
```

## ☁️ Azure Deployment

### ACR Push
```powershell
# Login
az acr login --name REGISTRY_NAME

# Build and push
az acr build --registry REGISTRY_NAME --image hacktoberfest-backend:latest ./backend
```

### Container Apps Deploy
```powershell
# Update app
az containerapp update --name backend --resource-group hacktoberfest-rg --image REGISTRY.azurecr.io/hacktoberfest-backend:latest

# View logs
az containerapp logs show --name backend --resource-group hacktoberfest-rg --follow
```

## 🗄️ Database Commands

### MongoDB
```powershell
# Connect
mongosh "mongodb://localhost:27017/hacktoberfest"

# Backup
mongodump --db hacktoberfest --out ./backup

# Restore
mongorestore --db hacktoberfest ./backup/hacktoberfest
```

### PostgreSQL
```powershell
# Connect
psql -U postgres -d hacktoberfest

# Backup
pg_dump hacktoberfest > backup.sql

# Restore
psql hacktoberfest < backup.sql
```

## 🔍 Monitoring & Debugging

### Check Health
```powershell
# Local
Invoke-WebRequest -Uri "http://localhost:3001/health"

# Docker
docker compose exec backend curl http://localhost:3001/health

# Cloud (replace URL)
curl https://your-app-url.com/health
```

### View Logs
```powershell
# Docker
docker compose logs -f backend

# AWS
aws logs tail /ecs/hacktoberfest --follow

# GCP
gcloud logging read "resource.type=cloud_run_revision" --limit 50 --format json

# Azure
az containerapp logs show --name backend --resource-group hacktoberfest-rg --follow
```

### Container Stats
```powershell
# Docker
docker compose stats

# Docker detailed
docker stats --no-stream

# Kubernetes
kubectl top pods
```

## 🧹 Cleanup Commands

### Local
```powershell
# Stop services
Stop-Process -Name "node" -Force
Stop-Service MongoDB
```

### Docker
```powershell
# Stop and remove
docker compose down -v

# Remove all
docker compose down -v --rmi all

# Prune system
docker system prune -a
```

### Cloud
```powershell
# AWS - Delete stack
aws cloudformation delete-stack --stack-name hacktoberfest

# GCP - Delete service
gcloud run services delete hacktoberfest-backend

# Azure - Delete resource group
az group delete --name hacktoberfest-rg --yes
```

## 🔐 Secrets Management

### Create Secrets
```powershell
# AWS
aws secretsmanager create-secret --name db-url --secret-string "mongodb://..."

# GCP
echo -n "mongodb://..." | gcloud secrets create db-url --data-file=-

# Azure
az keyvault secret set --vault-name hacktoberfest-kv --name db-url --value "mongodb://..."
```

### Retrieve Secrets
```powershell
# AWS
aws secretsmanager get-secret-value --secret-id db-url --query SecretString --output text

# GCP
gcloud secrets versions access latest --secret="db-url"

# Azure
az keyvault secret show --vault-name hacktoberfest-kv --name db-url --query value -o tsv
```

## 📊 Useful One-Liners

### Find Port Usage
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 3001).OwningProcess
```

### Kill Process on Port
```powershell
Stop-Process -Id (Get-NetTCPConnection -LocalPort 3001).OwningProcess -Force
```

### Check Node/npm Version
```powershell
node --version; npm --version
```

### Clean npm Cache
```powershell
npm cache clean --force
```

### Rebuild node_modules
```powershell
Remove-Item -Recurse -Force node_modules; npm install
```

### Check Docker Disk Usage
```powershell
docker system df
```

### Test API Endpoint
```powershell
Invoke-WebRequest -Uri "http://localhost:3001/api/endpoint" -Method GET
```

### Get Container IP
```powershell
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' CONTAINER_NAME
```

### Export Environment Variables
```powershell
Get-Content .env | ForEach-Object { $name, $value = $_.Split('='); [Environment]::SetEnvironmentVariable($name, $value) }
```

---

**Quick Reference Guide**  
For detailed instructions, see the comprehensive deployment guides in the same directory.

Last Updated: October 2025
