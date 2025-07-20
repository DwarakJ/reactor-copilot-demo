# Azure Deployment Guide for ABC Sports Centre

## Overview

This guide provides a comprehensive deployment plan for the ABC Sports Centre application to Azure using the recommended architecture pattern:

- **Backend (FastAPI)**: Azure App Service (Linux)
- **Frontend (React)**: Azure Static Web Apps
- **CI/CD**: GitHub Actions

This architecture follows Microsoft Learn best practices for deploying full-stack applications to Azure.

## Architecture Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   User/Browser  │────▶│ Azure Static Web │────▶│ Azure App       │
│                 │     │ Apps (React)     │     │ Service (API)   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                                │                           │
                                ▼                           ▼
                        ┌──────────────────┐     ┌─────────────────┐
                        │ Azure CDN        │     │ Application     │
                        │ (Global Edge)    │     │ Insights        │
                        └──────────────────┘     └─────────────────┘
```

## Benefits of This Architecture

1. **Cost Optimization**: Static Web Apps is cheaper for hosting React applications
2. **Performance**: CDN integration for faster global content delivery
3. **Scalability**: App Service provides automatic scaling for the API
4. **Security**: Built-in authentication options with Static Web Apps
5. **DevOps**: Integrated CI/CD with GitHub Actions

## Azure Resources Required

### 1. Azure App Service (Backend)
- **SKU**: B1 (Basic) minimum for production
- **Runtime**: Python 3.12
- **OS**: Linux
- **Features**: Deployment slots, Application Insights, Custom domains

### 2. Azure Static Web Apps (Frontend)
- **SKU**: Free tier (suitable for most use cases)
- **Features**: CDN, Custom domains, GitHub integration
- **Build preset**: React

### 3. Azure Application Insights (Optional but recommended)
- **Purpose**: Monitoring and diagnostics
- **Integration**: Both frontend and backend telemetry

## Prerequisites

Before deployment, ensure you have:

1. **Azure Subscription** with appropriate permissions
2. **Azure CLI** installed and configured
3. **GitHub Repository** with the application code
4. **GitHub Account** with admin access to the repository

## Step-by-Step Implementation Plan

### Phase 1: Prepare Application for Azure

#### 1.1 Backend Preparation

1. **Add production-ready dependencies** to `backend/requirements.txt`:
   ```txt
   fastapi
   uvicorn[standard]
   gunicorn
   ```

2. **Create startup script** `backend/startup.sh`:
   ```bash
   #!/bin/bash
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
   ```

3. **Environment configuration** - Update `backend/main.py` for production:
   ```python
   import os
   from fastapi import FastAPI
   from fastapi.middleware.cors import CORSMiddleware
   
   app = FastAPI(title="ABC Sports Centre Activities API")
   
   # Production-ready CORS configuration
   allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
   
   app.add_middleware(
       CORSMiddleware,
       allow_origins=allowed_origins,
       allow_methods=["GET", "POST"],
       allow_headers=["*"],
   )
   ```

#### 1.2 Frontend Preparation

1. **Update build configuration** in `frontend/package.json`:
   ```json
   {
     "homepage": ".",
     "scripts": {
       "build": "react-scripts build"
     }
   }
   ```

2. **Environment variable handling** - Update API URL configuration:
   ```javascript
   const API_URL = process.env.REACT_APP_API_URL || 
                   process.env.NODE_ENV === 'production' 
                   ? 'https://your-backend-app.azurewebsites.net'
                   : 'http://localhost:8000';
   ```

### Phase 2: Deploy Backend to Azure App Service

#### 2.1 Create App Service via Azure CLI

```bash
# Create resource group
az group create --name abc-sports-rg --location "East US"

# Create App Service plan
az appservice plan create \
  --name abc-sports-plan \
  --resource-group abc-sports-rg \
  --sku B1 \
  --is-linux

# Create App Service
az webapp create \
  --resource-group abc-sports-rg \
  --plan abc-sports-plan \
  --name abc-sports-api \
  --runtime "PYTHON|3.12" \
  --deployment-source-url https://github.com/your-username/reactor-copilot-demo \
  --deployment-source-branch main
```

#### 2.2 Configure App Service Settings

```bash
# Set startup command
az webapp config set \
  --resource-group abc-sports-rg \
  --name abc-sports-api \
  --startup-file "backend/startup.sh"

# Configure environment variables
az webapp config appsettings set \
  --resource-group abc-sports-rg \
  --name abc-sports-api \
  --settings ALLOWED_ORIGINS="https://your-frontend-app.azurestaticapps.net"
```

### Phase 3: Deploy Frontend to Azure Static Web Apps

#### 3.1 Create Static Web App

```bash
# Create Static Web App
az staticwebapp create \
  --name abc-sports-frontend \
  --resource-group abc-sports-rg \
  --source https://github.com/your-username/reactor-copilot-demo \
  --location "East US 2" \
  --branch main \
  --app-location "frontend" \
  --output-location "build"
```

#### 3.2 Configure Build Settings

The Static Web App will automatically create a GitHub Actions workflow. Update the generated file:

```yaml
# .github/workflows/azure-static-web-apps-*.yml
name: Azure Static Web Apps CI/CD

on:
  push:
    branches:
      - main
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches:
      - main

jobs:
  build_and_deploy_job:
    if: github.event_name == 'push' || (github.event_name == 'pull_request' && github.event.action != 'closed')
    runs-on: ubuntu-latest
    name: Build and Deploy Job
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: true
      - name: Build And Deploy
        id: builddeploy
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: "upload"
          app_location: "frontend"
          output_location: "build"
        env:
          REACT_APP_API_URL: "https://abc-sports-api.azurewebsites.net"
```

### Phase 4: Set Up Continuous Deployment

#### 4.1 Backend CI/CD with GitHub Actions

Create `.github/workflows/backend-deploy.yml`:

```yaml
name: Deploy Backend to Azure App Service

on:
  push:
    branches: [ main ]
    paths: [ 'backend/**' ]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
        
    - name: Install dependencies
      run: |
        cd backend
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        
    - name: Deploy to Azure App Service
      uses: azure/webapps-deploy@v2
      with:
        app-name: 'abc-sports-api'
        publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
        package: './backend'
```

#### 4.2 Configure GitHub Secrets

Add these secrets to your GitHub repository:

1. `AZURE_WEBAPP_PUBLISH_PROFILE`: Download from Azure Portal → App Service → Get publish profile
2. `AZURE_STATIC_WEB_APPS_API_TOKEN`: Automatically created by Static Web Apps

### Phase 5: Environment Configuration

#### 5.1 Production Environment Variables

**Backend (App Service Application Settings):**
```bash
ALLOWED_ORIGINS=https://your-frontend-app.azurestaticapps.net
ENVIRONMENT=production
```

**Frontend (Static Web Apps):**
```bash
REACT_APP_API_URL=https://abc-sports-api.azurewebsites.net
```

### Phase 6: Testing and Verification

#### 6.1 Backend Testing

1. **Health Check**:
   ```bash
   curl https://abc-sports-api.azurewebsites.net/activities
   ```

2. **API Documentation**:
   Visit `https://abc-sports-api.azurewebsites.net/docs`

#### 6.2 Frontend Testing

1. **Static Web App URL**: 
   Visit the generated URL from Azure Portal

2. **Functionality Test**:
   - Browse activities
   - Test enrollment form
   - Verify API integration

#### 6.3 End-to-End Testing

1. **Cross-Origin Requests**: Verify CORS is properly configured
2. **Error Handling**: Test with invalid data
3. **Performance**: Check load times and API response times

## Security Considerations

### 6.1 CORS Configuration
- Restrict allowed origins to your Static Web App domain
- Avoid using wildcards (`*`) in production

### 6.2 Environment Variables
- Never commit sensitive data to Git
- Use Azure Key Vault for secrets in production
- Rotate API keys regularly

### 6.3 HTTPS
- Both services automatically provide HTTPS
- Ensure all API calls use HTTPS URLs

## Monitoring and Maintenance

### 7.1 Application Insights Setup

```bash
# Enable Application Insights
az webapp config appsettings set \
  --resource-group abc-sports-rg \
  --name abc-sports-api \
  --settings APPLICATIONINSIGHTS_CONNECTION_STRING="your-connection-string"
```

### 7.2 Log Monitoring

- **App Service Logs**: Available in Azure Portal → Log Stream
- **Static Web Apps**: Built-in analytics dashboard
- **GitHub Actions**: Deployment logs and history

## Cost Optimization

### 8.1 Estimated Monthly Costs

- **App Service B1**: ~$13.14/month
- **Static Web Apps (Free tier)**: $0/month
- **Application Insights**: ~$2-5/month (based on usage)

**Total estimated cost**: ~$15-20/month

### 8.2 Cost-Saving Tips

1. Use **Dev/Test pricing** for development environments
2. Configure **auto-scaling** rules to scale down during low usage
3. Use **deployment slots** for staging (included in Basic tier)

## Troubleshooting Guide

### 9.1 Common Issues

**Backend not starting:**
- Check startup command in App Service configuration
- Verify Python version compatibility
- Review application logs

**Frontend not connecting to backend:**
- Verify CORS configuration
- Check API URL environment variable
- Ensure HTTPS is used for production

**GitHub Actions failing:**
- Verify secrets are correctly configured
- Check file paths in workflow
- Review build logs for errors

## References

- [Quickstart: Deploy a Python web app to Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python)
- [Deploy a React app on Azure Static Web Apps](https://learn.microsoft.com/en-us/azure/static-web-apps/deploy-react)
- [Deploy to Azure App Service using GitHub Actions](https://learn.microsoft.com/en-us/azure/app-service/deploy-github-actions)
- [Azure Static Web Apps documentation](https://learn.microsoft.com/en-us/azure/static-web-apps/)
- [Azure App Service documentation](https://learn.microsoft.com/en-us/azure/app-service/)

## Next Steps

After reviewing this guide:

1. **Create Azure resources** using the provided CLI commands
2. **Configure GitHub secrets** for automated deployment
3. **Test the deployment** end-to-end
4. **Set up monitoring** with Application Insights
5. **Configure custom domains** if needed

This architecture provides a production-ready, scalable, and cost-effective solution for deploying the ABC Sports Centre application to Azure.