# Scrum Master AI - Helm Chart

This directory contains the Helm chart and Helmfile configuration for deploying the Scrum Master AI Agent application to Kubernetes.

## Prerequisites

- Kubernetes cluster (1.24+)
- Helm 3.x
- Helmfile (optional, for multi-environment deployments)
- kubectl configured to access your cluster

## Chart Structure

```
helm/
├── scrum-master-ai/          # Main Helm chart
│   ├── Chart.yaml            # Chart metadata
│   ├── values.yaml           # Default values
│   ├── templates/            # Kubernetes manifest templates
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   ├── configmap.yaml
│   │   ├── secret.yaml
│   │   ├── ingress.yaml
│   │   ├── serviceaccount.yaml
│   │   ├── hpa.yaml
│   │   └── _helpers.tpl
│   └── .helmignore
└── environments/             # Environment-specific configurations
    ├── development/
    ├── staging/
    └── production/
```

## Quick Start

### 1. Install with Helm (single environment)

```bash
# Create namespace
kubectl create namespace scrum-master-ai

# Create required secrets
kubectl create secret generic scrum-master-ai-secrets \
  --from-literal=anthropic-api-key=YOUR_ANTHROPIC_API_KEY \
  -n scrum-master-ai

# Optional: Create Slack secrets (if using Slack integration)
kubectl create secret generic scrum-master-ai-slack-secrets \
  --from-literal=bot-token=YOUR_SLACK_BOT_TOKEN \
  --from-literal=app-token=YOUR_SLACK_APP_TOKEN \
  --from-literal=signing-secret=YOUR_SLACK_SIGNING_SECRET \
  -n scrum-master-ai

# Install the chart
helm install scrum-master-ai ./helm/scrum-master-ai \
  --namespace scrum-master-ai \
  --values ./helm/scrum-master-ai/values.yaml
```

### 2. Install with Helmfile (multi-environment)

```bash
# Install to development environment
helmfile -e development apply

# Install to staging environment
helmfile -e staging apply

# Install to production environment
helmfile -e production apply
```

## Configuration

### Key Configuration Values

| Parameter | Description | Default |
|-----------|-------------|---------|
| `replicaCount` | Number of replicas | `1` |
| `image.repository` | Image repository | `scrum-master-ai` |
| `image.tag` | Image tag | `""` (uses appVersion) |
| `app.debug` | Enable debug mode | `false` |
| `app.anthropic.modelName` | Claude model name | `claude-sonnet-4-5-20250929` |
| `app.slack.enabled` | Enable Slack integration | `false` |
| `postgresql.enabled` | Enable PostgreSQL dependency | `true` |
| `ingress.enabled` | Enable ingress | `false` |

### Environment Variables

The application requires the following secrets:

1. **Anthropic API Key** (required)
   - Secret: `scrum-master-ai-secrets`
   - Key: `anthropic-api-key`

2. **Slack Credentials** (optional, if `app.slack.enabled: true`)
   - Secret: `scrum-master-ai-slack-secrets`
   - Keys: `bot-token`, `app-token`, `signing-secret`

## Deployment Workflows

### Development Deployment

```bash
# Update image and deploy
helm upgrade --install scrum-master-ai ./helm/scrum-master-ai \
  --namespace scrum-master-ai-dev \
  --create-namespace \
  --values ./helm/environments/development/values.yaml \
  --set image.tag=latest

# Check deployment status
kubectl get pods -n scrum-master-ai-dev
```

### Staging Deployment

```bash
helmfile -e staging apply

# Or with Helm directly
helm upgrade --install scrum-master-ai ./helm/scrum-master-ai \
  --namespace scrum-master-ai-staging \
  --create-namespace \
  --values ./helm/environments/staging/values.yaml \
  --set image.tag=staging
```

### Production Deployment

```bash
# IMPORTANT: Ensure secrets are properly configured
helmfile -e production apply

# Or with Helm directly
helm upgrade --install scrum-master-ai ./helm/scrum-master-ai \
  --namespace scrum-master-ai-prod \
  --create-namespace \
  --values ./helm/environments/production/values.yaml \
  --set image.tag=v0.1.0
```

## Managing Secrets

### Using kubectl (Development)

```bash
kubectl create secret generic scrum-master-ai-secrets \
  --from-literal=anthropic-api-key=sk-ant-xxxxx \
  -n scrum-master-ai-dev
```

### Using Sealed Secrets (Recommended for GitOps)

```bash
# Install sealed-secrets controller first
# Then create a sealed secret
kubectl create secret generic scrum-master-ai-secrets \
  --from-literal=anthropic-api-key=sk-ant-xxxxx \
  --dry-run=client -o yaml | \
  kubeseal -o yaml > sealed-secret.yaml

kubectl apply -f sealed-secret.yaml -n scrum-master-ai-prod
```

### Using SOPS (Recommended for Helmfile)

```bash
# Encrypt secrets file
sops -e -i ./helm/environments/production/secrets.yaml

# Deploy with helmfile (automatically decrypts)
helmfile -e production apply
```

## Upgrading

```bash
# Upgrade with Helm
helm upgrade scrum-master-ai ./helm/scrum-master-ai \
  --namespace scrum-master-ai \
  --values ./helm/scrum-master-ai/values.yaml

# Upgrade with Helmfile
helmfile -e production apply
```

## Uninstalling

```bash
# With Helm
helm uninstall scrum-master-ai -n scrum-master-ai

# With Helmfile
helmfile -e production destroy
```

## Troubleshooting

### Check pod status

```bash
kubectl get pods -n scrum-master-ai
kubectl describe pod <pod-name> -n scrum-master-ai
kubectl logs <pod-name> -n scrum-master-ai
```

### Check ingress

```bash
kubectl get ingress -n scrum-master-ai
kubectl describe ingress scrum-master-ai -n scrum-master-ai
```

### Verify secrets

```bash
kubectl get secrets -n scrum-master-ai
kubectl describe secret scrum-master-ai-secrets -n scrum-master-ai
```

### Database connectivity

```bash
# Port-forward to PostgreSQL
kubectl port-forward svc/scrum-master-ai-postgresql 5432:5432 -n scrum-master-ai

# Connect using psql
psql -h localhost -U rum -d rum
```

## Security Best Practices

1. **Never commit unencrypted secrets** to version control
2. Use **Sealed Secrets**, **SOPS**, or cloud provider secret managers for production
3. Enable **network policies** to restrict traffic between pods
4. Use **RBAC** to limit service account permissions
5. Regularly **update dependencies** and scan for vulnerabilities
6. Enable **pod security policies** or **pod security standards**
7. Use **private container registries** for production images

## CI/CD Integration

### Example GitHub Actions workflow

```yaml
name: Deploy to Production
on:
  push:
    tags:
      - 'v*'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install helmfile
        run: |
          wget https://github.com/helmfile/helmfile/releases/download/v0.157.0/helmfile_0.157.0_linux_amd64.tar.gz
          tar xzf helmfile_*.tar.gz
          sudo mv helmfile /usr/local/bin/

      - name: Configure kubectl
        run: |
          echo "${{ secrets.KUBECONFIG }}" | base64 -d > kubeconfig
          export KUBECONFIG=./kubeconfig

      - name: Deploy to production
        run: |
          export KUBECONFIG=./kubeconfig
          helmfile -e production apply
```

## Support

For issues or questions, please refer to the main project README or create an issue in the repository.
