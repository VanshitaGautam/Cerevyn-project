# Azure deployment plan

## Suggested architecture
- Azure App Service for the FastAPI web application.
- Azure Monitor / Application Insights for logs and telemetry.
- Azure SQL or another managed persistent database for production data.
- GitHub Actions for CI and manually triggered deployment using OpenID Connect (OIDC).

## Important limitations of the local demo
The default database is a local SQLite file. It is suitable for local development and a single-instance demo, but it is not a good production database for a scaled or ephemeral cloud deployment. Use a managed database and configure `DATABASE_URL` before production deployment. Add authentication/authorization to approval routes before exposing them.

## Deployment checklist
1. Create an Azure App Service that supports Python 3.12.
2. Configure a GitHub Actions OIDC federated credential for the Azure identity.
3. Add repository secrets `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, and `AZURE_SUBSCRIPTION_ID`.
4. Add repository variable `AZURE_WEBAPP_NAME`.
5. Configure the App Service startup command as `uvicorn app.main:app --host 0.0.0.0 --port 8000` if required by the selected hosting configuration.
6. Set a persistent managed database connection string as `DATABASE_URL`.
7. Review logs, health checks, secrets, access control, and deployment settings before production use.

The workflow in `.github/workflows/deploy.yml` is a template. It does not create Azure resources or configure identity for you.
