# 🐳 Containerized Deployment Guide (Docker)

This comprehensive guide covers deploying the Hacktoberfest-2025 project using Docker and Docker Compose for consistent, isolated environments across development, staging, and production.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Docker Basics](#docker-basics)
3. [Building Docker Images](#building-docker-images)
4. [Docker Compose Setup](#docker-compose-setup)
5. [Multi-Service Architecture](#multi-service-architecture)
6. [Configuration Management](#configuration-management)
7. [Networking and Volumes](#networking-and-volumes)
8. [Production Optimization](#production-optimization)
9. [Monitoring and Logging](#monitoring-and-logging)
10. [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

### Required Software

| Software | Version | Download Link |
|----------|---------|---------------|
| **Docker Desktop** | Latest | [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop) |
| **Docker Compose** | v2.x | Included with Docker Desktop |
| **Git** | Latest | [git-scm.com](https://git-scm.com/downloads) |

### System Requirements

- **Windows 10/11** (Pro, Enterprise, or Education)
- **8GB RAM** minimum (16GB recommended)
- **20GB** free disk space
- **WSL 2** enabled (Docker Desktop requirement)

### Verify Installation

```powershell
# Check Docker
docker --version
docker compose version

# Check Docker is running
docker ps

# Verify Docker resources
docker system info
```

## 🐋 Docker Basics

### Understanding Docker Components

```
┌─────────────────────────────────────┐
│         Docker Desktop              │
├─────────────────────────────────────┤
│  Docker Engine    │  Docker Compose │
├─────────────────────────────────────┤
│    Containers (Running Apps)        │
├─────────────────────────────────────┤
│    Images (Blueprints)              │
├─────────────────────────────────────┤
│    Volumes (Data Storage)           │
├─────────────────────────────────────┤
│    Networks (Communication)         │
└─────────────────────────────────────┘
```

### Key Concepts

- **Image**: Template for creating containers
- **Container**: Running instance of an image
- **Volume**: Persistent data storage
- **Network**: Container communication
- **Compose**: Multi-container orchestration

## 🏗️ Building Docker Images

### Backend Dockerfile (Node.js/TypeScript)

Create `backend/Dockerfile`:

```dockerfile
# Multi-stage build for optimized image size
# Stage 1: Build
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./
COPY tsconfig.json ./

# Install dependencies (including dev dependencies for build)
RUN npm ci

# Copy source code
COPY src ./src

# Build TypeScript code
RUN npm run build

# Stage 2: Production
FROM node:18-alpine

# Install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install only production dependencies
RUN npm ci --only=production && npm cache clean --force

# Copy built files from builder stage
COPY --from=builder /app/dist ./dist

# Change ownership to non-root user
RUN chown -R nodejs:nodejs /app

# Switch to non-root user
USER nodejs

# Expose port
EXPOSE 3001

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD node -e "require('http').get('http://localhost:3001/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

# Use dumb-init to handle signals properly
ENTRYPOINT ["dumb-init", "--"]

# Start application
CMD ["node", "dist/index.js"]
```

### Backend Dockerfile (Python/Flask)

Create `backend/Dockerfile.python`:

```dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -u 1001 flaskuser

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Change ownership
RUN chown -R flaskuser:flaskuser /app

# Switch to non-root user
USER flaskuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Run application
CMD ["python", "app.py"]
```

### Frontend Dockerfile (Next.js)

Create `frontend/Dockerfile`:

```dockerfile
# Stage 1: Dependencies
FROM node:18-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Stage 2: Builder
FROM node:18-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build Next.js application
ENV NEXT_TELEMETRY_DISABLED 1
RUN npm run build

# Stage 3: Runner
FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001

# Copy necessary files
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

RUN chown -R nextjs:nodejs /app

USER nextjs

EXPOSE 3000

ENV PORT 3000

HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \
  CMD node -e "require('http').get('http://localhost:3000', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"

CMD ["node", "server.js"]
```

### Building Images

```powershell
# Build backend image
docker build -t hacktoberfest-backend:latest -f backend/Dockerfile ./backend

# Build Python backend
docker build -t hacktoberfest-python:latest -f backend/Dockerfile.python ./backend

# Build frontend image
docker build -t hacktoberfest-frontend:latest -f frontend/Dockerfile ./frontend

# Build all with specific tags
docker build -t hacktoberfest-backend:v1.0.0 ./backend
docker build -t hacktoberfest-frontend:v1.0.0 ./frontend

# View built images
docker images
```

## 🎼 Docker Compose Setup

### Complete docker-compose.yml

Create `docker-compose.yml` in project root:

```yaml
version: '3.9'

services:
  # MongoDB Database
  mongodb:
    image: mongo:7
    container_name: hacktoberfest-mongodb
    restart: unless-stopped
    environment:
      MONGO_INITDB_ROOT_USERNAME: ${MONGO_USERNAME:-admin}
      MONGO_INITDB_ROOT_PASSWORD: ${MONGO_PASSWORD:-securepassword}
      MONGO_INITDB_DATABASE: ${MONGO_DATABASE:-hacktoberfest}
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db
      - mongodb_config:/data/configdb
      - ./mongo-init.js:/docker-entrypoint-initdb.d/mongo-init.js:ro
    networks:
      - app-network
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017/test --quiet
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 40s

  # PostgreSQL Database (for Python backend)
  postgres:
    image: postgres:15-alpine
    container_name: hacktoberfest-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-pguser}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-pgpassword}
      POSTGRES_DB: ${POSTGRES_DB:-hacktoberfest}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./postgres-init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-pguser}"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Backend (Node.js/TypeScript)
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: hacktoberfest-backend
    restart: unless-stopped
    environment:
      NODE_ENV: ${NODE_ENV:-production}
      PORT: 3001
      DATABASE_URL: mongodb://${MONGO_USERNAME:-admin}:${MONGO_PASSWORD:-securepassword}@mongodb:27017/${MONGO_DATABASE:-hacktoberfest}?authSource=admin
      JWT_SECRET: ${JWT_SECRET:-change-this-secret-in-production}
      JWT_EXPIRES_IN: ${JWT_EXPIRES_IN:-7d}
      CORS_ORIGIN: ${CORS_ORIGIN:-http://localhost:3000}
      API_RATE_LIMIT: ${API_RATE_LIMIT:-100}
      LOG_LEVEL: ${LOG_LEVEL:-info}
    ports:
      - "3001:3001"
    volumes:
      - ./backend/logs:/app/logs
    depends_on:
      mongodb:
        condition: service_healthy
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "node", "-e", "require('http').get('http://localhost:3001/health', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Backend Python (Flask)
  backend-python:
    build:
      context: ./backend
      dockerfile: Dockerfile.python
    container_name: hacktoberfest-python
    restart: unless-stopped
    environment:
      FLASK_ENV: ${FLASK_ENV:-production}
      DATABASE_URL: postgresql://${POSTGRES_USER:-pguser}:${POSTGRES_PASSWORD:-pgpassword}@postgres:5432/${POSTGRES_DB:-hacktoberfest}
      SECRET_KEY: ${FLASK_SECRET:-change-this-flask-secret}
      JWT_SECRET_KEY: ${FLASK_JWT_SECRET:-change-this-jwt-secret}
    ports:
      - "5000:5000"
    depends_on:
      postgres:
        condition: service_healthy
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "python -c \"import urllib.request; urllib.request.urlopen('http://localhost:5000/health')\" || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Frontend (Next.js)
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      args:
        NEXT_PUBLIC_API_URL: ${NEXT_PUBLIC_API_URL:-http://localhost:3001}
    container_name: hacktoberfest-frontend
    restart: unless-stopped
    environment:
      NEXT_PUBLIC_API_URL: ${NEXT_PUBLIC_API_URL:-http://localhost:3001}
      NEXT_PUBLIC_ENVIRONMENT: ${NEXT_PUBLIC_ENVIRONMENT:-production}
    ports:
      - "3000:3000"
    depends_on:
      - backend
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "node", "-e", "require('http').get('http://localhost:3000', (r) => {process.exit(r.statusCode === 200 ? 0 : 1)})"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Redis Cache (Optional)
  redis:
    image: redis:7-alpine
    container_name: hacktoberfest-redis
    restart: unless-stopped
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    command: redis-server --appendonly yes

  # Nginx Reverse Proxy (Optional)
  nginx:
    image: nginx:alpine
    container_name: hacktoberfest-nginx
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
    depends_on:
      - frontend
      - backend
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  app-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16

volumes:
  mongodb_data:
    driver: local
  mongodb_config:
    driver: local
  postgres_data:
    driver: local
  redis_data:
    driver: local
```

### Development docker-compose Override

Create `docker-compose.dev.yml`:

```yaml
version: '3.9'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.dev
    volumes:
      - ./backend/src:/app/src
      - ./backend/node_modules:/app/node_modules
    environment:
      NODE_ENV: development
      LOG_LEVEL: debug
    command: npm run dev

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    volumes:
      - ./frontend:/app
      - /app/node_modules
      - /app/.next
    environment:
      NODE_ENV: development
    command: npm run dev

  backend-python:
    volumes:
      - ./backend:/app
    environment:
      FLASK_ENV: development
      FLASK_DEBUG: 1
```

## 🎯 Running Docker Compose

### Start All Services

```powershell
# Start all services in detached mode
docker compose up -d

# Start with build
docker compose up --build -d

# Start specific services
docker compose up -d mongodb backend frontend

# Development mode with override
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# View logs
docker compose logs -f

# View specific service logs
docker compose logs -f backend
```

### Stop and Cleanup

```powershell
# Stop all services
docker compose stop

# Stop and remove containers
docker compose down

# Remove volumes too (WARNING: deletes data)
docker compose down -v

# Remove images
docker compose down --rmi all

# Complete cleanup
docker compose down -v --rmi all --remove-orphans
```

### Service Management

```powershell
# Restart specific service
docker compose restart backend

# View service status
docker compose ps

# View resource usage
docker compose stats

# Execute command in container
docker compose exec backend sh

# View container logs
docker compose logs backend --tail=100 --follow
```

## 🔧 Configuration Management

### Environment Variables File

Create `.env` in project root:

```env
# Application
NODE_ENV=production
FLASK_ENV=production

# MongoDB
MONGO_USERNAME=admin
MONGO_PASSWORD=super_secure_password_change_me
MONGO_DATABASE=hacktoberfest

# PostgreSQL
POSTGRES_USER=pguser
POSTGRES_PASSWORD=secure_pg_password_change_me
POSTGRES_DB=hacktoberfest

# Backend
JWT_SECRET=super_secret_jwt_key_min_32_chars
JWT_EXPIRES_IN=7d
CORS_ORIGIN=http://localhost:3000
API_RATE_LIMIT=100
LOG_LEVEL=info

# Flask
FLASK_SECRET=flask_secret_key_change_me
FLASK_JWT_SECRET=flask_jwt_secret_change_me

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:3001
NEXT_PUBLIC_ENVIRONMENT=production
```

### Docker Secrets (Production)

For sensitive data in production:

```powershell
# Create secrets
"my-secret-password" | docker secret create db_password -

# Use in compose file
services:
  backend:
    secrets:
      - db_password

secrets:
  db_password:
    external: true
```

## 🌐 Networking and Volumes

### Custom Network Configuration

```yaml
networks:
  frontend-network:
    driver: bridge
  backend-network:
    driver: bridge
    internal: true  # No external access

services:
  frontend:
    networks:
      - frontend-network
  backend:
    networks:
      - frontend-network
      - backend-network
  database:
    networks:
      - backend-network  # Only accessible by backend
```

### Volume Management

```powershell
# List volumes
docker volume ls

# Inspect volume
docker volume inspect hacktoberfest-2025_mongodb_data

# Backup volume
docker run --rm -v hacktoberfest-2025_mongodb_data:/data -v ${PWD}/backup:/backup alpine tar czf /backup/mongodb-backup.tar.gz /data

# Restore volume
docker run --rm -v hacktoberfest-2025_mongodb_data:/data -v ${PWD}/backup:/backup alpine tar xzf /backup/mongodb-backup.tar.gz -C /

# Remove unused volumes
docker volume prune
```

## ⚡ Production Optimization

### Dockerfile Best Practices

1. **Multi-stage builds** - Reduce image size
2. **Layer caching** - Order instructions by change frequency
3. **.dockerignore** - Exclude unnecessary files
4. **Non-root user** - Security best practice
5. **Health checks** - Enable container health monitoring

### Create .dockerignore

```
# Dependencies
node_modules/
venv/
__pycache__/

# Development
*.log
*.md
!README.md
.git/
.gitignore
.env*
.vscode/
.idea/

# Build artifacts
dist/
build/
*.pyc
*.pyo

# Documentation
docs/
*.md
LICENSE

# Testing
tests/
*.test.js
coverage/

# OS files
.DS_Store
Thumbs.db
```

### Resource Limits

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

### Logging Configuration

```yaml
services:
  backend:
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
        labels: "app=backend"
```

## 📊 Monitoring and Logging

### View Real-time Logs

```powershell
# All services
docker compose logs -f --tail=100

# Specific service
docker compose logs -f backend

# With timestamps
docker compose logs -f --timestamps backend

# Follow logs from multiple services
docker compose logs -f backend frontend mongodb
```

### Container Stats

```powershell
# All containers
docker compose stats

# Continuous monitoring
docker compose stats --no-stream
```

### Health Checks

```powershell
# Check health status
docker compose ps

# Inspect health
docker inspect --format='{{.State.Health.Status}}' hacktoberfest-backend

# View health check logs
docker inspect --format='{{json .State.Health}}' hacktoberfest-backend
```

## 🐛 Troubleshooting

### Common Issues

#### Issue 1: Container Won't Start

**Problem:** Container exits immediately

**Solutions:**
```powershell
# Check logs
docker compose logs backend

# Check exit code
docker compose ps

# Inspect container
docker inspect hacktoberfest-backend

# Check configuration
docker compose config
```

#### Issue 2: Database Connection Failed

**Problem:** Backend can't connect to database

**Solutions:**
```powershell
# Check if database is healthy
docker compose ps

# Test database connectivity
docker compose exec backend ping mongodb

# Check environment variables
docker compose exec backend printenv | grep DATABASE

# Verify network
docker network inspect hacktoberfest-2025_app-network

# Check database logs
docker compose logs mongodb
```

#### Issue 3: Port Already in Use

**Problem:** `port is already allocated`

**Solutions:**
```powershell
# Find process using port
Get-Process -Id (Get-NetTCPConnection -LocalPort 3001).OwningProcess

# Stop conflicting service
Stop-Process -Id <PID> -Force

# Or change port in docker-compose.yml
ports:
  - "3002:3001"
```

#### Issue 4: Out of Disk Space

**Problem:** `no space left on device`

**Solutions:**
```powershell
# Clean up unused resources
docker system prune -a

# Remove unused volumes
docker volume prune

# Remove specific items
docker image prune -a
docker container prune

# Check disk usage
docker system df
```

#### Issue 5: Build Cache Issues

**Problem:** Changes not reflected in container

**Solutions:**
```powershell
# Build without cache
docker compose build --no-cache

# Force recreation
docker compose up --force-recreate --build

# Remove and rebuild
docker compose down
docker compose up --build
```

#### Issue 6: Permission Denied Errors

**Problem:** Permission errors in containers

**Solutions:**
```powershell
# Check file ownership
docker compose exec backend ls -la

# Fix permissions
docker compose exec --user root backend chown -R nodejs:nodejs /app

# Or in Dockerfile, set correct user
RUN chown -R nodejs:nodejs /app
USER nodejs
```

#### Issue 7: Slow Performance

**Problem:** Containers running slow

**Solutions:**
```powershell
# Increase Docker Desktop resources
# Settings → Resources → Advanced

# Check resource usage
docker compose stats

# Optimize build with multi-stage
# Use layer caching effectively
# Remove unnecessary dependencies
```

### Debug Commands

```powershell
# Enter container shell
docker compose exec backend sh

# Run commands as root
docker compose exec --user root backend sh

# View container processes
docker compose exec backend ps aux

# Check network connectivity
docker compose exec backend ping mongodb

# View environment variables
docker compose exec backend printenv

# Check mounted volumes
docker compose exec backend df -h
```

### Validate Configuration

```powershell
# Validate compose file
docker compose config

# Check syntax
docker compose config --quiet

# View resolved configuration
docker compose config --services
```

## 🚀 Advanced Topics

### Docker Registry

```powershell
# Tag image for registry
docker tag hacktoberfest-backend:latest registry.example.com/hacktoberfest-backend:latest

# Push to registry
docker push registry.example.com/hacktoberfest-backend:latest

# Pull from registry
docker pull registry.example.com/hacktoberfest-backend:latest
```

### Container Orchestration

For production at scale, consider:
- **Docker Swarm** - Simple orchestration
- **Kubernetes** - Enterprise-grade orchestration
- **AWS ECS/Fargate** - Managed container service
- **Google Cloud Run** - Serverless containers

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Security Best Practices](https://docs.docker.com/engine/security/)

## 🆘 Getting Help

1. Check [deployment README](./README.md)
2. Review [troubleshooting section](#troubleshooting)
3. Search [GitHub issues](https://github.com/hari7261/Hacktoberfest-2025/issues)
4. Open new issue with container logs and configuration

---

**Happy Deploying! 🐳**

Last Updated: October 2025
