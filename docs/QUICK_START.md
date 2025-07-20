# Azure Deployment Quick Start

## Prerequisites Checklist

- [ ] Azure subscription with appropriate permissions
- [ ] Azure CLI installed and logged in (`az login`)
- [ ] GitHub repository cloned and accessible
- [ ] Admin access to the GitHub repository for secrets configuration

## Quick Deployment Steps

### 1. Create Azure Resources

```bash
# Login to Azure
az login

# Create resource group
az group create --name abc-sports-rg --location "East US"

# Create App Service plan
az appservice plan create \
  --name abc-sports-plan \
  --resource-group abc-sports-rg \
  --sku B1 \
  --is-linux

# Create App Service for backend
az webapp create \
  --resource-group abc-sports-rg \
  --plan abc-sports-plan \
  --name abc-sports-api-<your-unique-suffix> \
  --runtime "PYTHON|3.12"

# Create Static Web App for frontend
az staticwebapp create \
  --name abc-sports-frontend-<your-unique-suffix> \
  --resource-group abc-sports-rg \
  --source https://github.com/<your-username>/reactor-copilot-demo \
  --location "East US 2" \
  --branch main \
  --app-location "frontend" \
  --output-location "build"
```

### 2. Configure App Service

```bash
# Set startup command
az webapp config set \
  --resource-group abc-sports-rg \
  --name abc-sports-api-<your-unique-suffix> \
  --startup-file "backend/startup.sh"

# Configure CORS settings
az webapp config appsettings set \
  --resource-group abc-sports-rg \
  --name abc-sports-api-<your-unique-suffix> \
  --settings ALLOWED_ORIGINS="https://abc-sports-frontend-<your-unique-suffix>.azurestaticapps.net"
```

### 3. Get URLs

```bash
# Get App Service URL
az webapp show \
  --resource-group abc-sports-rg \
  --name abc-sports-api-<your-unique-suffix> \
  --query "defaultHostName" \
  --output tsv

# Get Static Web App URL
az staticwebapp show \
  --name abc-sports-frontend-<your-unique-suffix> \
  --resource-group abc-sports-rg \
  --query "defaultHostname" \
  --output tsv
```

### 4. Configure GitHub Secrets

1. Go to your GitHub repository
2. Navigate to Settings → Secrets and variables → Actions
3. Add the following secrets:

   **For Backend Deployment:**
   - `AZURE_WEBAPP_PUBLISH_PROFILE`: 
     ```bash
     az webapp deployment list-publishing-profiles \
       --resource-group abc-sports-rg \
       --name abc-sports-api-<your-unique-suffix> \
       --xml
     ```

   **For Frontend Deployment:**
   - `AZURE_STATIC_WEB_APPS_API_TOKEN`: 
     ```bash
     az staticwebapp secrets list \
       --name abc-sports-frontend-<your-unique-suffix> \
       --resource-group abc-sports-rg \
       --query "properties.apiKey" \
       --output tsv
     ```

### 5. Update Configuration

Update the frontend API URL in the GitHub Actions workflow file:

`.github/workflows/frontend-deploy.yml`:
```yaml
env:
  REACT_APP_API_URL: "https://abc-sports-api-<your-unique-suffix>.azurewebsites.net"
```

### 6. Deploy

1. Commit and push your changes:
   ```bash
   git add .
   git commit -m "Configure Azure deployment"
   git push origin main
   ```

2. GitHub Actions will automatically deploy both frontend and backend

### 7. Test Deployment

1. **Backend API**: Visit `https://abc-sports-api-<your-unique-suffix>.azurewebsites.net/docs`
2. **Frontend App**: Visit `https://abc-sports-frontend-<your-unique-suffix>.azurestaticapps.net`
3. **End-to-end test**: Try enrolling in an activity through the frontend

## Verification Checklist

- [ ] Backend API responds at `/activities` endpoint
- [ ] Backend API documentation available at `/docs`
- [ ] Frontend loads and displays activities
- [ ] Frontend can successfully submit enrollment forms
- [ ] CORS is properly configured (no console errors)
- [ ] Both HTTP and HTTPS work correctly

## Troubleshooting

### Common Issues:

1. **Backend not starting**: Check App Service logs in Azure Portal
2. **CORS errors**: Verify ALLOWED_ORIGINS setting in App Service
3. **GitHub Actions failing**: Check repository secrets are configured correctly
4. **Frontend not connecting**: Verify REACT_APP_API_URL in the deployment workflow

### Useful Commands:

```bash
# View App Service logs
az webapp log tail --resource-group abc-sports-rg --name abc-sports-api-<your-unique-suffix>

# Restart App Service
az webapp restart --resource-group abc-sports-rg --name abc-sports-api-<your-unique-suffix>

# Check deployment status
az webapp deployment list --resource-group abc-sports-rg --name abc-sports-api-<your-unique-suffix>
```

## Cost Management

- **App Service B1**: ~$13/month
- **Static Web Apps**: Free tier
- **Total**: ~$13-15/month

To minimize costs:
- Use Dev/Test pricing for non-production environments
- Configure auto-scaling to scale down during low usage
- Monitor usage through Azure Cost Management

## Next Steps

After successful deployment:

1. Configure custom domain names (optional)
2. Set up Application Insights for monitoring
3. Configure deployment slots for staging
4. Set up alerts for monitoring and security
5. Review and optimize performance