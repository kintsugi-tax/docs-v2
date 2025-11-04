# Deployment Automation Guide

This guide explains how to set up automated deployment for the Kintsugi documentation site with a merged API reference.

## 🎯 Overview

The documentation site uses a **single merged OpenAPI file** that combines:
- **Customer API**: All standard customer-facing endpoints
- **Public Partners API**: Only endpoints listed in the "API Reference - Partners" section

The merged file is automatically updated and deployed when changes are detected. Mintlify generates a single MCP server at `/mcp` with all available endpoints.

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
1. Fetches Customer API spec
2. Fetches Partners API spec
3. Merges Customer API + Public Partners endpoints
4. Adds MCP configuration to all endpoints
5. Generates documentation from merged spec
6. Commits changes if updates detected
7. Deploys to Mintlify
```

### 2. Merged OpenAPI Generation

The system creates a single merged OpenAPI file:

```bash
# Merged OpenAPI file (openapi.json)
- Contains all Customer API endpoints
- Contains public Partners API endpoints (from "API Reference - Partners")
- All endpoints have MCP enabled
- Single MCP server at /mcp
```

### 3. Navigation Structure

The `docs.json` includes a single OpenAPI reference:

```json
{
  "openapi": [
    {
      "url": "./openapi.json",
      "label": "API Reference"
    }
  ]
}
```

The merged OpenAPI file includes endpoints from both APIs, organized in the documentation navigation.

## 📋 Manual Deployment Steps

### Option 1: Local Development

```bash
# Navigate to docs-v2 directory
cd /path/to/docs-v2

# Download API specs
curl -o openapi-customer.json https://api-doc.trykintsugi.com/openapi.json
curl -o openapi-partners.json https://api.trykintsugi.com/openapi.json

# Create merged OpenAPI file
cp openapi-customer.json openapi.json
python3 scripts/create-merged-openapi.py

# Generate API reference documentation
./scripts/generate-api-docs.sh

# Start local development server
mintlify dev
```

### Option 2: Direct Mintlify Deployment

```bash
# Download specs and create merged file (see Option 1)
# Then deploy to Mintlify
mintlify deploy
```

## 🔄 Update Process

### Automatic Updates
- **Frequency**: Every 6 hours
- **Trigger**: API spec changes detected
- **Process**: 
  1. Fetch latest Customer API spec
  2. Fetch latest Partners API spec
  3. Extract public Partners endpoints from "API Reference - Partners"
  4. Merge Customer API + Public Partners endpoints
  5. Add MCP configuration
  6. Generate documentation
  7. Commit changes
  8. Deploy to Mintlify

### Manual Updates
- **Trigger**: Manual workflow dispatch
- **Process**: Same as automatic, but on-demand

## 🛠️ Configuration Files

### 1. GitHub Actions Workflow
**File**: `.github/workflows/update-api-docs.yml`

**Key Features**:
- Downloads Customer API spec
- Downloads Partners API spec
- Runs `create-merged-openapi.py` to merge specs
- Generates documentation from merged file
- Commits changes automatically
- Deploys to Mintlify

### 2. Merge Script
**File**: `scripts/create-merged-openapi.py`

**Key Features**:
- Reads `docs.json` to find "API Reference - Partners" pages
- Extracts OpenAPI paths from MDX files
- Filters Partners API to public endpoints only
- Merges Customer API + filtered Partners API
- Adds MCP configuration to all endpoints

### 3. Generation Script
**File**: `scripts/generate-api-docs.sh`

**Key Features**:
- Generates MDX files from merged OpenAPI spec
- Creates organized directory structure
- Provides detailed output

### 4. Documentation Configuration
**File**: `docs.json`

**Key Features**:
- Single OpenAPI configuration (merged file)
- Navigation organized by API sections
- "API Reference - Partners" section defines which Partners endpoints are public

## 📊 Monitoring and Troubleshooting

### Success Indicators
- ✅ GitHub Actions workflow completes successfully
- ✅ Merged OpenAPI file created with MCP config
- ✅ API reference generates without errors
- ✅ Mintlify deployment succeeds
- ✅ MCP server available at `/mcp` with all endpoints

### Common Issues

#### 1. OpenAPI Spec Unavailable
```bash
# Check API availability
curl -s https://api-doc.trykintsugi.com/openapi.json | jq '.info'
curl -s https://api.trykintsugi.com/openapi.json | jq '.info'
```

#### 2. Merge Errors
```bash
# Run merge script manually
python3 scripts/create-merged-openapi.py

# Check for errors in output
# Verify docs.json structure
# Ensure MDX files have correct openapi: frontmatter
```

#### 3. Partners Endpoints Missing
- Verify endpoint is listed in `docs.json` under "API Reference - Partners"
- Check MDX file exists with correct `openapi:` frontmatter
- Run merge script to verify endpoint is included

#### 4. MCP Server Issues
- Verify merged `openapi.json` has `x-mint.mcp.enabled: true`
- Check all endpoints have endpoint-level MCP config
- Verify MCP server in Mintlify dashboard

### Debugging Commands

```bash
# Check merged OpenAPI file
jq '.paths | length' openapi.json
jq '."x-mint".mcp.enabled' openapi.json

# Verify Partners endpoints included
jq '.paths | keys | map(select(. | startswith("/v1/")))' openapi.json

# Check generated files
find reference/api -name "*.mdx" | wc -l

# Test local development
mintlify dev
```

## 🎯 Best Practices

### 1. Regular Monitoring
- Check GitHub Actions status weekly
- Monitor Mintlify deployment logs
- Verify MCP server has all expected endpoints

### 2. Content Updates
- Update `docs.json` when adding new API groups
- Ensure Partners endpoints are listed in "API Reference - Partners" to be included in MCP
- Test locally before pushing changes
- Use descriptive commit messages

### 3. API Spec Management
- Keep OpenAPI specs up-to-date in backend
- Monitor for breaking changes
- Test documentation generation regularly

### 4. Partners Endpoint Management
- Only endpoints in "API Reference - Partners" are included in merged file
- Add Partners endpoints to `docs.json` to make them public
- Create MDX files with correct `openapi:` frontmatter

## 🚀 Deployment Checklist

### Before Deployment
- [ ] Customer API spec is accessible
- [ ] Partners API spec is accessible
- [ ] GitHub Actions workflow is configured
- [ ] Mintlify project is set up
- [ ] Local testing passes
- [ ] Merged OpenAPI file validates correctly

### After Deployment
- [ ] API reference is visible
- [ ] Navigation works correctly
- [ ] All Customer API endpoints are documented
- [ ] Public Partners API endpoints are documented
- [ ] MCP server at `/mcp` includes all endpoints
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
- Check merge script output
- Test local development server

### MCP Server Issues
- See `MCP_TROUBLESHOOTING.md` for detailed guidance
- Verify MCP configuration in merged OpenAPI file
- Check Mintlify dashboard → MCP Server section

## 🔗 Related Files

- `.github/workflows/update-api-docs.yml` - GitHub Actions workflow
- `scripts/create-merged-openapi.py` - Merge script
- `scripts/generate-api-docs.sh` - API generation script
- `docs.json` - Mintlify configuration
- `openapi.json` - Merged OpenAPI spec (generated)
- `MCP_SETUP.md` - MCP configuration guide
- `MCP_TROUBLESHOOTING.md` - MCP troubleshooting guide

---

**Last Updated**: $(date)
**Version**: 2.0.0
**Maintainer**: Kintsugi Documentation Team
