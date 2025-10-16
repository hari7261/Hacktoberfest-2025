# 🚀 Deployment Guides

Welcome to the comprehensive deployment documentation for Hacktoberfest-2025! This guide covers everything you need to deploy the application across different environments with detailed configuration, troubleshooting, and best practices.

## 📋 Table of Contents

1. [Local Development Deployment](./local.md)
2. [Containerized Deployment (Docker)](./containerized.md)
3. [Cloud Deployment](./cloud.md)
4. [Configuration Reference](#configuration-reference)
5. [Troubleshooting](#troubleshooting)

## 🎯 Quick Start

Choose your deployment environment:

### 🏠 Local Development
Perfect for development and testing on your local machine.
- **Best for**: Active development, debugging, quick iterations
- **Prerequisites**: Node.js, Python, Git
- **Time to deploy**: 5-10 minutes
- [→ Go to Local Deployment Guide](./local.md)

### 🐳 Containerized (Docker)
Run the entire stack in isolated containers.
- **Best for**: Consistent environments, team collaboration, staging
- **Prerequisites**: Docker Desktop
- **Time to deploy**: 10-15 minutes
- [→ Go to Containerized Deployment Guide](./containerized.md)

### ☁️ Cloud Production
Deploy to cloud providers for production workloads.
- **Best for**: Production deployments, scalability, high availability
- **Prerequisites**: Cloud provider account, Docker
- **Time to deploy**: 20-30 minutes
- [→ Go to Cloud Deployment Guide](./cloud.md)

## 📁 Project Architecture

The repository consists of multiple services and components:

```
Hacktoberfest-2025/
├── backend/              # Node.js/TypeScript API + Python Flask services
│   ├── src/             # TypeScript source files
│   ├── app.py           # Python Flask application
│   └── package.json     # Node.js dependencies
├── frontend/            # React/Next.js frontend application
├── docs/                # Documentation
├── docker-compose.yml   # Multi-container orchestration
└── Various language projects (Java, C++, Python, etc.)
```

## 🔧 Configuration Reference

### Environment Variables

#### Backend (Node.js/TypeScript)
```env
NODE_ENV=development|production
PORT=3001
DATABASE_URL=mongodb://localhost:27017/hacktoberfest
JWT_SECRET=your-secret-key-here
API_RATE_LIMIT=100
CORS_ORIGIN=http://localhost:3000
```

#### Backend (Python/Flask)
```env
FLASK_ENV=development|production
FLASK_APP=app.py
DATABASE_URL=postgresql://user:pass@localhost:5432/db
SECRET_KEY=your-flask-secret-key
JWT_SECRET_KEY=your-jwt-secret
```

#### Frontend
```env
NEXT_PUBLIC_API_URL=http://localhost:3001
NEXT_PUBLIC_ENVIRONMENT=development|production
```

### Database Configuration

#### MongoDB (for Node.js backend)
```yaml
Version: 7.x
Port: 27017
Authentication: Enabled in production
Connection String: mongodb://username:password@host:port/database
```

#### PostgreSQL (for Python backend)
```yaml
Version: 15.x
Port: 5432
Authentication: Required
Connection String: postgresql://username:password@host:port/database
```

## 🐛 Troubleshooting

### Common Issues Across All Environments

#### Port Already in Use
**Problem**: Error message "Port 3000 is already in use"

**Solutions**:
```powershell
# Windows PowerShell - Find process using port
Get-Process -Id (Get-NetTCPConnection -LocalPort 3000).OwningProcess

# Kill the process
Stop-Process -Id <PID> -Force

# Or change port in .env file
PORT=3002
```

#### Database Connection Failed
**Problem**: Cannot connect to database

**Solutions**:
1. Verify database is running
2. Check connection string format
3. Verify network connectivity
4. Check firewall rules
5. Verify credentials

#### Module Not Found Errors
**Problem**: Missing dependencies

**Solutions**:
```powershell
# Node.js
Remove-Item -Recurse -Force node_modules
Remove-Item package-lock.json
npm install

# Python
pip install -r requirements.txt --force-reinstall
```

### Performance Issues

#### Slow Startup Times
- Clear Docker build cache: `docker system prune -a`
- Increase Docker Desktop memory allocation
- Use `.dockerignore` to exclude unnecessary files
- Implement multi-stage builds

#### High Memory Usage
- Limit container resources in docker-compose
- Enable production mode (`NODE_ENV=production`)
- Optimize database queries
- Implement caching strategies

## 🔐 Security Best Practices

### Development
- Never commit `.env` files to version control
- Use different secrets for dev/staging/prod
- Keep dependencies updated
- Use HTTPS in production

### Production
- Enable rate limiting
- Implement CORS properly
- Use environment-specific secrets
- Enable database authentication
- Use SSL/TLS for all connections
- Implement logging and monitoring
- Regular security audits

## 📊 Monitoring and Logging

### Local Development
```javascript
// Use Morgan for HTTP logging
app.use(morgan('dev'));

// Console logging
console.log('[INFO]', 'Server started on port', PORT);
```

### Production
- Use structured logging (JSON format)
- Implement log aggregation (ELK, CloudWatch, etc.)
- Set up health check endpoints
- Monitor application metrics
- Configure alerts for critical errors

## 🚦 Health Checks

Implement these endpoints in your applications:

```javascript
// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date() });
});

// Readiness check (includes dependencies)
app.get('/ready', async (req, res) => {
  const dbConnected = await checkDatabase();
  res.json({ 
    status: dbConnected ? 'ready' : 'not ready',
    database: dbConnected 
  });
});
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)
- [12-Factor App Methodology](https://12factor.net/)
- [Security Best Practices](./security-best-practices.md)

## 🆘 Getting Help

If you encounter issues not covered in these guides:

1. Check the [GitHub Issues](https://github.com/hari7261/Hacktoberfest-2025/issues)
2. Review the [Contributing Guide](../../CONTRIBUTING.md)
3. Join our community discussions
4. Open a new issue with detailed information

## 📝 Contributing to Documentation

Found an error or want to improve these guides? Contributions are welcome!

1. Fork the repository
2. Make your changes
3. Submit a pull request
4. Tag with `documentation` label

---

**Last Updated**: October 2025  
**Maintainers**: Hacktoberfest 2025 Contributors