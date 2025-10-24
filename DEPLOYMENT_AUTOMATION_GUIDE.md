# Deployment Automation Guide

This guide explains how to set up automated deployment for the Kintsugi documentation site with dual API references.

## 🎯 Overview

The documentation site now supports **two separate API references**:
- **Customer API**: Standard customer-facing endpoints
- **Partners API**: Comprehensive partner integration endpoints

Both APIs are automatically updated and deployed when changes are detected.

## 🔧 Setup Requirements

### Prerequisites
- GitHub repository with `docs-v2` as the main branch
- Mintlify account and project configured
- GitHub Actions enabled

### API Endpoints
- **Customer API**: `https://api-doc.trykintsugi.com/openapi.json`
- **Partners API**: `https://api.trykintsugi.com/openapi.json`

## 🚀 Automated Deployment Process

### 1. GitHub Actions Workflow

The `.github/workflows/update-api-docs.yml` workflow automatically:

```yaml
# Triggers
- Schedule: Every 6 hours
- Manual: workflow_dispatch
- Push: Changes to scripts or docs.json

# Actions
1. Fetches both OpenAPI specs
2. Generates documentation for both APIs
3. Commits changes if updates detected
4. Deploys to Mintlify
```

### 2. Dual API Generation

The system generates documentation for both APIs:

```bash
# Customer API (Standard endpoints)
reference/api/
├── customers/
├── transactions/
├── tax-estimation/
└── ...

# Partners API (Comprehensive endpoints)
reference/partners/
├── customers/
├── transactions/
├── organizations/
├── connections/
├── admin/
└── ...
```

### 3. Navigation Structure

The `docs.json` includes both API references:

```json
{
  "openapi": [
    {
      "url": "./openapi.json",
      "label": "Customer API"
    },
    {
      "url": "./openapi-partners.json", 
      "label": "Partners API"
    }
  ]
}
```

## 📋 Manual Deployment Steps

### Option 1: Local Development

```bash
# Navigate to docs-v2 directory
cd /path/to/docs-v2

# Generate both API references
./scripts/generate-api-docs.sh

# Start local development server
mintlify dev
```

### Option 2: Direct Mintlify Deployment

```bash
# Generate API docs
./scripts/generate-api-docs.sh

# Deploy to Mintlify
mintlify deploy
```

## 🔄 Update Process

### Automatic Updates
- **Frequency**: Every 6 hours
- **Trigger**: API spec changes detected
- **Process**: 
  1. Fetch latest OpenAPI specs
  2. Generate documentation
  3. Commit changes
  4. Deploy to Mintlify

### Manual Updates
- **Trigger**: Manual workflow dispatch
- **Process**: Same as automatic, but on-demand

## 🛠️ Configuration Files

### 1. GitHub Actions Workflow
**File**: `.github/workflows/update-api-docs.yml`

**Key Features**:
- Fetches both OpenAPI specs
- Generates documentation for both APIs
- Commits changes automatically
- Deploys to Mintlify

### 2. Generation Script
**File**: `scripts/generate-api-docs.sh`

**Key Features**:
- Downloads both OpenAPI specs
- Generates MDX files for both APIs
- Creates organized directory structure
- Provides detailed output

### 3. Documentation Configuration
**File**: `docs.json`

**Key Features**:
- Dual OpenAPI configuration
- Separate navigation tabs
- Organized API groupings
- Partner integration sections

## 📊 Monitoring and Troubleshooting

### Success Indicators
- ✅ GitHub Actions workflow completes successfully
- ✅ Both API references generate without errors
- ✅ Mintlify deployment succeeds
- ✅ Documentation site shows both API tabs

### Common Issues

#### 1. OpenAPI Spec Unavailable
```bash
# Check API availability
curl -s https://api-doc.trykintsugi.com/openapi.json | jq '.info'
curl -s https://api.trykintsugi.com/openapi.json | jq '.info'
```

#### 2. Generation Errors
```bash
# Run generation script manually
./scripts/generate-api-docs.sh

# Check for errors in output
```

#### 3. Navigation Issues
- Verify `docs.json` syntax
- Check file paths in navigation
- Ensure generated files exist

### Debugging Commands

```bash
# Check generated files
find reference/ -name "*.mdx" | wc -l

# Verify OpenAPI specs
ls -la openapi*.json

# Test local development
mintlify dev
```

## 🎯 Best Practices

### 1. Regular Monitoring
- Check GitHub Actions status weekly
- Monitor Mintlify deployment logs
- Verify both API references are current

### 2. Content Updates
- Update `docs.json` when adding new API groups
- Test locally before pushing changes
- Use descriptive commit messages

### 3. API Spec Management
- Keep OpenAPI specs up-to-date in backend
- Monitor for breaking changes
- Test documentation generation regularly

## 🚀 Deployment Checklist

### Before Deployment
- [ ] Both OpenAPI specs are accessible
- [ ] GitHub Actions workflow is configured
- [ ] Mintlify project is set up
- [ ] Local testing passes

### After Deployment
- [ ] Both API references are visible
- [ ] Navigation works correctly
- [ ] All endpoints are documented
- [ ] Search functionality works

## 📞 Support

### GitHub Actions Issues
- Check workflow logs in GitHub
- Verify repository permissions
- Ensure secrets are configured

### Mintlify Issues
- Check Mintlify dashboard
- Review deployment logs
- Contact Mintlify support if needed

### API Documentation Issues
- Verify OpenAPI spec validity
- Check file generation process
- Test local development server

## 🔗 Related Files

- `.github/workflows/update-api-docs.yml` - GitHub Actions workflow
- `scripts/generate-api-docs.sh` - API generation script
- `docs.json` - Mintlify configuration
- `openapi.json` - Customer API spec (generated)
- `openapi-partners.json` - Partners API spec (generated)

---

**Last Updated**: $(date)
**Version**: 1.0.0
**Maintainer**: Kintsugi Documentation Team
