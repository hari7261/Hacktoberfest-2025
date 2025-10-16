# ☁️ Cloud Deployment Guide

This comprehensive guide covers deploying the Hacktoberfest-2025 project to major cloud providers including AWS, Google Cloud Platform (GCP), and Microsoft Azure. The guide focuses on container-based deployments for consistency and scalability.

## 📋 Table of Contents

1. [Overview](#overview)
2. [Pre-Deployment Checklist](#pre-deployment-checklist)
3. [AWS Deployment](#aws-deployment)
4. [Google Cloud Platform](#google-cloud-platform)
5. [Microsoft Azure](#microsoft-azure)
6. [Database Services](#database-services)
7. [CI/CD Integration](#cicd-integration)
8. [Monitoring and Observability](#monitoring-and-observability)
9. [Security Best Practices](#security-best-practices)
10. [Cost Optimization](#cost-optimization)
11. [Troubleshooting](#troubleshooting)

## 🌐 Overview

### Cloud Deployment Architecture

```
┌─────────────────────────────────────────────────────┐
│                 Cloud Provider                       │
├─────────────────────────────────────────────────────┤
│  Load Balancer / CDN                                │
├──────────────────┬──────────────────┬───────────────┤
│   Frontend       │   Backend API    │   Database    │
│  (Container)     │   (Container)    │   (Managed)   │
├──────────────────┴──────────────────┴───────────────┤
│  Container Registry │ Secrets Manager │ Monitoring  │
└─────────────────────────────────────────────────────┘
```

### Recommended Services by Provider

| Component | AWS | GCP | Azure |
|-----------|-----|-----|-------|
| **Compute** | ECS Fargate / EKS | Cloud Run / GKE | Container Apps / AKS |
| **Database** | RDS / DocumentDB | Cloud SQL / Firestore | Azure Database / Cosmos DB |
| **Storage** | S3 | Cloud Storage | Blob Storage |
| **Registry** | ECR | Container Registry | ACR |
| **Secrets** | Secrets Manager | Secret Manager | Key Vault |
| **Monitoring** | CloudWatch | Cloud Monitoring | Azure Monitor |
| **CDN** | CloudFront | Cloud CDN | Azure CDN |

## ✅ Pre-Deployment Checklist

### 1. Prepare Your Application

```powershell
# Build and test locally first
docker compose build
docker compose up -d
docker compose ps

# Run tests
docker compose exec backend npm test
docker compose exec frontend npm test

# Verify health checks work
Invoke-WebRequest -Uri "http://localhost:3001/health"
```

### 2. Environment Configuration

Create cloud-specific `.env.production`:

```env
# Production Environment
NODE_ENV=production
FLASK_ENV=production

# Database (use managed service connection strings)
DATABASE_URL=<cloud-database-url>

# Security (use strong secrets)
JWT_SECRET=<generated-secret-min-32-chars>
FLASK_SECRET=<generated-secret>

# API Configuration
CORS_ORIGIN=https://your-domain.com
API_RATE_LIMIT=100

# Logging
LOG_LEVEL=info
SENTRY_DSN=<your-sentry-dsn>
```

### 3. Container Registry Setup

Each cloud provider needs images in their registry:

```powershell
# Tag images for cloud registry
docker tag hacktoberfest-backend:latest <registry-url>/hacktoberfest-backend:v1.0.0
docker tag hacktoberfest-frontend:latest <registry-url>/hacktoberfest-frontend:v1.0.0
```

## 🚀 AWS Deployment

### Option 1: AWS ECS Fargate (Recommended for Simplicity)

#### Step 1: Install AWS CLI

```powershell
# Install AWS CLI
winget install Amazon.AWSCLI

# Configure credentials
aws configure
# Enter: Access Key ID, Secret Access Key, Region (e.g., us-east-1), Output format (json)

# Verify
aws sts get-caller-identity
```

#### Step 2: Create ECR Repositories

```powershell
# Create repository for backend
aws ecr create-repository --repository-name hacktoberfest-backend --region us-east-1

# Create repository for frontend
aws ecr create-repository --repository-name hacktoberfest-frontend --region us-east-1

# Get login credentials
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
```

#### Step 3: Push Images to ECR

```powershell
# Set variables
$ACCOUNT_ID = (aws sts get-caller-identity --query Account --output text)
$REGION = "us-east-1"
$BACKEND_IMAGE = "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/hacktoberfest-backend:latest"
$FRONTEND_IMAGE = "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/hacktoberfest-frontend:latest"

# Tag and push backend
docker tag hacktoberfest-backend:latest $BACKEND_IMAGE
docker push $BACKEND_IMAGE

# Tag and push frontend
docker tag hacktoberfest-frontend:latest $FRONTEND_IMAGE
docker push $FRONTEND_IMAGE
```

#### Step 4: Create ECS Cluster

```powershell
# Create cluster
aws ecs create-cluster --cluster-name hacktoberfest-cluster --region us-east-1

# Create task execution role (if not exists)
aws iam create-role --role-name ecsTaskExecutionRole --assume-role-policy-document file://trust-policy.json
```

Create `trust-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

#### Step 5: Create Task Definition

Create `backend-task-def.json`:

```json
{
  "family": "hacktoberfest-backend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::<account-id>:role/ecsTaskExecutionRole",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "<account-id>.dkr.ecr.us-east-1.amazonaws.com/hacktoberfest-backend:latest",
      "portMappings": [
        {
          "containerPort": 3001,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "NODE_ENV", "value": "production"},
        {"name": "PORT", "value": "3001"}
      ],
      "secrets": [
        {
          "name": "DATABASE_URL",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:<account-id>:secret:db-url"
        },
        {
          "name": "JWT_SECRET",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:<account-id>:secret:jwt-secret"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/hacktoberfest-backend",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:3001/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ]
}
```

Register task definition:

```powershell
aws ecs register-task-definition --cli-input-json file://backend-task-def.json
```

#### Step 6: Create ECS Service

```powershell
# Create service
aws ecs create-service `
  --cluster hacktoberfest-cluster `
  --service-name backend-service `
  --task-definition hacktoberfest-backend `
  --desired-count 2 `
  --launch-type FARGATE `
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx,subnet-yyy],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

#### Step 7: Set Up Application Load Balancer

```powershell
# Create load balancer
aws elbv2 create-load-balancer `
  --name hacktoberfest-alb `
  --subnets subnet-xxx subnet-yyy `
  --security-groups sg-xxx `
  --scheme internet-facing

# Create target group
aws elbv2 create-target-group `
  --name hacktoberfest-backend-tg `
  --protocol HTTP `
  --port 3001 `
  --vpc-id vpc-xxx `
  --target-type ip `
  --health-check-path /health

# Create listener
aws elbv2 create-listener `
  --load-balancer-arn <alb-arn> `
  --protocol HTTP `
  --port 80 `
  --default-actions Type=forward,TargetGroupArn=<target-group-arn>
```

### Option 2: AWS App Runner (Simplest)

```powershell
# Create App Runner service
aws apprunner create-service `
  --service-name hacktoberfest-backend `
  --source-configuration "{
    ImageRepository: {
      ImageIdentifier: '$BACKEND_IMAGE',
      ImageRepositoryType: 'ECR',
      ImageConfiguration: {
        Port: '3001',
        RuntimeEnvironmentVariables: {
          NODE_ENV: 'production'
        }
      }
    },
    AutoDeploymentsEnabled: true
  }" `
  --instance-configuration "{
    Cpu: '1 vCPU',
    Memory: '2 GB'
  }"
```

## 🌟 Google Cloud Platform

### Option 1: Cloud Run (Recommended)

#### Step 1: Install gcloud CLI

```powershell
# Download and install from: cloud.google.com/sdk/docs/install

# Initialize
gcloud init

# Set project
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

#### Step 2: Build and Push to Container Registry

```powershell
# Configure Docker for GCR
gcloud auth configure-docker

# Set variables
$PROJECT_ID = (gcloud config get-value project)
$REGION = "us-central1"

# Build and push using Cloud Build
gcloud builds submit --tag gcr.io/$PROJECT_ID/hacktoberfest-backend ./backend
gcloud builds submit --tag gcr.io/$PROJECT_ID/hacktoberfest-frontend ./frontend
```

#### Step 3: Deploy to Cloud Run

```powershell
# Deploy backend
gcloud run deploy hacktoberfest-backend `
  --image gcr.io/$PROJECT_ID/hacktoberfest-backend `
  --platform managed `
  --region $REGION `
  --allow-unauthenticated `
  --set-env-vars NODE_ENV=production `
  --set-secrets DATABASE_URL=db-url:latest,JWT_SECRET=jwt-secret:latest `
  --memory 1Gi `
  --cpu 1 `
  --max-instances 10 `
  --min-instances 1 `
  --port 3001

# Deploy frontend
gcloud run deploy hacktoberfest-frontend `
  --image gcr.io/$PROJECT_ID/hacktoberfest-frontend `
  --platform managed `
  --region $REGION `
  --allow-unauthenticated `
  --set-env-vars NEXT_PUBLIC_API_URL=https://backend-url.run.app `
  --memory 512Mi `
  --port 3000

# Get service URLs
gcloud run services list
```

#### Step 4: Set Up Cloud SQL (MongoDB Atlas or PostgreSQL)

```powershell
# Create Cloud SQL instance
gcloud sql instances create hacktoberfest-db `
  --database-version=POSTGRES_15 `
  --tier=db-f1-micro `
  --region=$REGION

# Create database
gcloud sql databases create hacktoberfest --instance=hacktoberfest-db

# Create user
gcloud sql users create dbuser `
  --instance=hacktoberfest-db `
  --password=secure-password

# Connect Cloud Run to Cloud SQL
gcloud run services update hacktoberfest-backend `
  --add-cloudsql-instances PROJECT_ID:REGION:hacktoberfest-db
```

#### Step 5: Set Up Custom Domain

```powershell
# Map custom domain
gcloud run domain-mappings create `
  --service hacktoberfest-backend `
  --domain api.yourdomain.com `
  --region $REGION

# Follow DNS instructions to add records
```

### Option 2: Google Kubernetes Engine (GKE)

```powershell
# Create GKE cluster
gcloud container clusters create hacktoberfest-cluster `
  --zone us-central1-a `
  --num-nodes 3 `
  --machine-type n1-standard-2 `
  --enable-autoscaling `
  --min-nodes 1 `
  --max-nodes 5

# Get credentials
gcloud container clusters get-credentials hacktoberfest-cluster --zone us-central1-a

# Deploy using kubectl
kubectl apply -f k8s/
```

## 🔷 Microsoft Azure

### Option 1: Azure Container Apps (Recommended)

#### Step 1: Install Azure CLI

```powershell
# Install Azure CLI
winget install Microsoft.AzureCLI

# Login
az login

# Set subscription
az account set --subscription "YOUR_SUBSCRIPTION_ID"
```

#### Step 2: Create Resources

```powershell
# Set variables
$RESOURCE_GROUP = "hacktoberfest-rg"
$LOCATION = "eastus"
$ACR_NAME = "hacktoberfestacr"
$ENV_NAME = "hacktoberfest-env"

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create Azure Container Registry
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic

# Login to ACR
az acr login --name $ACR_NAME
```

#### Step 3: Build and Push Images

```powershell
# Build and push to ACR
az acr build --registry $ACR_NAME --image hacktoberfest-backend:latest ./backend
az acr build --registry $ACR_NAME --image hacktoberfest-frontend:latest ./frontend

# Or use Docker
$ACR_URL = "$ACR_NAME.azurecr.io"
docker tag hacktoberfest-backend:latest $ACR_URL/hacktoberfest-backend:latest
docker push $ACR_URL/hacktoberfest-backend:latest
```

#### Step 4: Create Container Apps Environment

```powershell
# Install Container Apps extension
az extension add --name containerapp --upgrade

# Create environment
az containerapp env create `
  --name $ENV_NAME `
  --resource-group $RESOURCE_GROUP `
  --location $LOCATION
```

#### Step 5: Deploy Container Apps

```powershell
# Deploy backend
az containerapp create `
  --name backend `
  --resource-group $RESOURCE_GROUP `
  --environment $ENV_NAME `
  --image $ACR_URL/hacktoberfest-backend:latest `
  --target-port 3001 `
  --ingress external `
  --registry-server $ACR_URL `
  --registry-username $ACR_NAME `
  --registry-password (az acr credential show --name $ACR_NAME --query passwords[0].value -o tsv) `
  --env-vars NODE_ENV=production `
  --cpu 1.0 `
  --memory 2.0Gi `
  --min-replicas 1 `
  --max-replicas 5

# Deploy frontend
az containerapp create `
  --name frontend `
  --resource-group $RESOURCE_GROUP `
  --environment $ENV_NAME `
  --image $ACR_URL/hacktoberfest-frontend:latest `
  --target-port 3000 `
  --ingress external `
  --registry-server $ACR_URL `
  --env-vars NEXT_PUBLIC_API_URL=https://backend.app.azurecontainerapps.io

# Get URLs
az containerapp show --name backend --resource-group $RESOURCE_GROUP --query properties.configuration.ingress.fqdn
```

#### Step 6: Set Up Azure Database

```powershell
# Create Azure Database for PostgreSQL
az postgres flexible-server create `
  --resource-group $RESOURCE_GROUP `
  --name hacktoberfest-db `
  --location $LOCATION `
  --admin-user dbadmin `
  --admin-password 'SecurePassword123!' `
  --sku-name Standard_B1ms `
  --tier Burstable `
  --version 15

# Create database
az postgres flexible-server db create `
  --resource-group $RESOURCE_GROUP `
  --server-name hacktoberfest-db `
  --database-name hacktoberfest

# Update container app with connection string
az containerapp update `
  --name backend `
  --resource-group $RESOURCE_GROUP `
  --set-env-vars DATABASE_URL=secretref:db-connection-string
```

### Option 2: Azure Kubernetes Service (AKS)

```powershell
# Create AKS cluster
az aks create `
  --resource-group $RESOURCE_GROUP `
  --name hacktoberfest-aks `
  --node-count 3 `
  --enable-addons monitoring `
  --generate-ssh-keys

# Get credentials
az aks get-credentials --resource-group $RESOURCE_GROUP --name hacktoberfest-aks

# Deploy
kubectl apply -f k8s/
```

## 🗄️ Database Services

### MongoDB Options

#### AWS DocumentDB

```powershell
aws docdb create-db-cluster `
  --db-cluster-identifier hacktoberfest-docdb `
  --engine docdb `
  --master-username admin `
  --master-user-password SecurePassword123
```

#### MongoDB Atlas (Multi-Cloud)

1. Visit [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create cluster on preferred cloud provider
3. Whitelist IP addresses or use VPC peering
4. Get connection string
5. Use in application:

```env
DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/hacktoberfest?retryWrites=true&w=majority
```

### PostgreSQL Options

#### AWS RDS

```powershell
aws rds create-db-instance `
  --db-instance-identifier hacktoberfest-db `
  --db-instance-class db.t3.micro `
  --engine postgres `
  --master-username admin `
  --master-user-password SecurePassword123 `
  --allocated-storage 20
```

#### GCP Cloud SQL

```powershell
gcloud sql instances create hacktoberfest-db `
  --database-version=POSTGRES_15 `
  --tier=db-f1-micro `
  --region=us-central1
```

#### Azure Database for PostgreSQL

```powershell
az postgres flexible-server create `
  --resource-group hacktoberfest-rg `
  --name hacktoberfest-db `
  --admin-user dbadmin `
  --admin-password 'SecurePassword123!'
```

## 🔄 CI/CD Integration

### GitHub Actions - AWS Deployment

Create `.github/workflows/deploy-aws.yml`:

```yaml
name: Deploy to AWS

on:
  push:
    branches: [main]

env:
  AWS_REGION: us-east-1
  ECR_REPOSITORY: hacktoberfest-backend
  ECS_SERVICE: backend-service
  ECS_CLUSTER: hacktoberfest-cluster
  ECS_TASK_DEFINITION: backend-task-def.json

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1

      - name: Build and push image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG ./backend
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG

      - name: Deploy to ECS
        run: |
          aws ecs update-service --cluster $ECS_CLUSTER --service $ECS_SERVICE --force-new-deployment
```

### GitHub Actions - GCP Deployment

Create `.github/workflows/deploy-gcp.yml`:

```yaml
name: Deploy to GCP Cloud Run

on:
  push:
    branches: [main]

env:
  PROJECT_ID: ${{ secrets.GCP_PROJECT_ID }}
  SERVICE_NAME: hacktoberfest-backend
  REGION: us-central1

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Cloud SDK
        uses: google-github-actions/setup-gcloud@v1
        with:
          service_account_key: ${{ secrets.GCP_SA_KEY }}
          project_id: ${{ secrets.GCP_PROJECT_ID }}

      - name: Configure Docker
        run: gcloud auth configure-docker

      - name: Build and Push
        run: |
          docker build -t gcr.io/$PROJECT_ID/$SERVICE_NAME:$GITHUB_SHA ./backend
          docker push gcr.io/$PROJECT_ID/$SERVICE_NAME:$GITHUB_SHA

      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy $SERVICE_NAME \
            --image gcr.io/$PROJECT_ID/$SERVICE_NAME:$GITHUB_SHA \
            --platform managed \
            --region $REGION \
            --allow-unauthenticated
```

### GitHub Actions - Azure Deployment

Create `.github/workflows/deploy-azure.yml`:

```yaml
name: Deploy to Azure

on:
  push:
    branches: [main]

env:
  AZURE_RESOURCE_GROUP: hacktoberfest-rg
  AZURE_CONTAINER_APP: backend
  ACR_NAME: hacktoberfestacr

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Azure Login
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Build and push to ACR
        run: |
          az acr build --registry $ACR_NAME \
            --image hacktoberfest-backend:${{ github.sha }} \
            ./backend

      - name: Deploy to Container Apps
        run: |
          az containerapp update \
            --name $AZURE_CONTAINER_APP \
            --resource-group $AZURE_RESOURCE_GROUP \
            --image $ACR_NAME.azurecr.io/hacktoberfest-backend:${{ github.sha }}
```

## 📊 Monitoring and Observability

### AWS CloudWatch

```powershell
# Create log group
aws logs create-log-group --log-group-name /ecs/hacktoberfest

# View logs
aws logs tail /ecs/hacktoberfest --follow

# Create metric alarm
aws cloudwatch put-metric-alarm `
  --alarm-name high-cpu `
  --alarm-description "CPU usage exceeds 80%" `
  --metric-name CPUUtilization `
  --namespace AWS/ECS `
  --statistic Average `
  --period 300 `
  --threshold 80 `
  --comparison-operator GreaterThanThreshold
```

### GCP Cloud Monitoring

```powershell
# View logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=hacktoberfest-backend" --limit 50

# Create uptime check
gcloud monitoring uptime create hacktoberfest-backend-check `
  --display-name="Backend Health Check" `
  --http-check-path=/health `
  --resource-type=uptime-url
```

### Azure Monitor

```powershell
# View logs
az monitor app-insights query `
  --app hacktoberfest-insights `
  --analytics-query "requests | where success == false | top 10 by timestamp desc"

# Create alert
az monitor metrics alert create `
  --name high-response-time `
  --resource-group hacktoberfest-rg `
  --scopes /subscriptions/.../resourceGroups/hacktoberfest-rg/providers/Microsoft.App/containerApps/backend `
  --condition "avg requests/duration > 1000" `
  --description "Response time exceeds 1 second"
```

## 🔐 Security Best Practices

### 1. Use Secrets Management

```powershell
# AWS Secrets Manager
aws secretsmanager create-secret --name db-url --secret-string "mongodb://..."

# GCP Secret Manager
echo -n "mongodb://..." | gcloud secrets create db-url --data-file=-

# Azure Key Vault
az keyvault secret set --vault-name hacktoberfest-kv --name db-url --value "mongodb://..."
```

### 2. Enable HTTPS/SSL

- Use managed certificates (AWS ACM, GCP Managed Certs, Azure App Service Certificates)
- Enforce HTTPS redirects
- Use HSTS headers

### 3. Network Security

- Use VPC/VNet for internal communication
- Implement security groups/firewall rules
- Use private endpoints for databases
- Enable DDoS protection

### 4. IAM and Access Control

- Follow principle of least privilege
- Use service accounts/managed identities
- Enable audit logging
- Implement MFA

### 5. Container Security

- Scan images for vulnerabilities
- Use minimal base images
- Run as non-root user
- Keep images updated

## 💰 Cost Optimization

### AWS Cost Optimization

```powershell
# Use Fargate Spot for non-critical workloads
# Enable auto-scaling
# Use Reserved Instances for predictable loads
# Set up billing alerts
aws budgets create-budget --account-id ACCOUNT_ID --budget file://budget.json
```

### GCP Cost Optimization

- Use committed use discounts
- Enable Cloud Run minimum instances only when needed
- Use Cloud Storage lifecycle policies
- Set up budget alerts

### Azure Cost Optimization

- Use Azure Reservations
- Enable auto-scaling
- Use Azure Hybrid Benefit
- Set up cost alerts

## 🐛 Troubleshooting

### Common Cloud Deployment Issues

#### Issue 1: Container Won't Start

**Solutions:**
```powershell
# AWS - Check ECS logs
aws logs tail /ecs/hacktoberfest --follow

# GCP - Check Cloud Run logs
gcloud logging read "resource.type=cloud_run_revision" --limit=50

# Azure - Check Container App logs
az containerapp logs show --name backend --resource-group hacktoberfest-rg
```

#### Issue 2: Database Connection Failed

- Verify security groups/firewall rules
- Check connection strings
- Verify VPC/VNet configuration
- Test with cloud shell/bastion host

#### Issue 3: High Latency

- Enable CDN for static assets
- Use appropriate instance sizes
- Optimize database queries
- Implement caching (Redis/Memcached)

#### Issue 4: Cost Overruns

- Review resource utilization
- Enable auto-scaling
- Use spot/preemptible instances
- Implement proper shutdown procedures

## 📚 Additional Resources

### AWS
- [AWS ECS Documentation](https://docs.aws.amazon.com/ecs/)
- [AWS App Runner Documentation](https://docs.aws.amazon.com/apprunner/)
- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)

### GCP
- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [GKE Documentation](https://cloud.google.com/kubernetes-engine/docs)
- [GCP Best Practices](https://cloud.google.com/architecture/best-practices)

### Azure
- [Azure Container Apps Documentation](https://docs.microsoft.com/azure/container-apps/)
- [AKS Documentation](https://docs.microsoft.com/azure/aks/)
- [Azure Architecture Center](https://docs.microsoft.com/azure/architecture/)

## 🆘 Getting Help

1. Check provider-specific documentation
2. Review [deployment README](./README.md)
3. Search provider forums
4. Open issue with deployment logs

---

**Deploy with Confidence! ☁️**

Last Updated: October 2025
