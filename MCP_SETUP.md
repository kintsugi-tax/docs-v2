# MCP (Model Context Protocol) Setup

This document explains how MCP is configured for the Kintsugi API documentation.

## Overview

The Model Context Protocol (MCP) enables AI tools (like Claude, Cursor, VS Code) to access your documentation and API endpoints. Our setup automatically enables MCP for all Customer API endpoints and public Partners API endpoints listed in the "API Reference - Partners" section.

## Configuration

MCP is configured at the file level in the merged `openapi.json` file using the `x-mint` extension:

```json
{
  "openapi": "3.1.0",
  "x-mint": {
    "mcp": {
      "enabled": true
    }
  },
  ...
}
```

The merged OpenAPI file includes:
- **Customer API endpoints** - All endpoints from the Customer API
- **Public Partners API endpoints** - Only endpoints listed in the "API Reference - Partners" section of `docs.json`

All endpoints in the merged file have MCP enabled. New endpoints that are added to either API will automatically be available as MCP tools once the OpenAPI spec is updated.

## Automatic Updates

The MCP configuration is automatically applied via:

**GitHub Actions Workflow** (`.github/workflows/update-api-docs.yml`):
- Runs every 6 hours
- Downloads Customer API spec from `https://api-doc.trykintsugi.com/openapi.json`
- Downloads Partners API spec from `https://api.trykintsugi.com/openapi.json`
- Extracts public Partners endpoints from "API Reference - Partners" section
- Merges Customer API + Public Partners endpoints into single `openapi.json`
- Automatically adds MCP configuration to all endpoints
- Regenerates documentation
- Commits changes if updates are detected

## How It Works

When the workflow runs:
1. Customer API spec is fetched from `https://api-doc.trykintsugi.com/openapi.json`
2. Partners API spec is fetched from `https://api.trykintsugi.com/openapi.json`
3. The `create-merged-openapi.py` script:
   - Reads `docs.json` to find all pages in "API Reference - Partners"
   - Extracts OpenAPI paths from MDX files
   - Filters Partners API to only include public endpoints
   - Merges Customer API + filtered Partners API into one file
   - Adds `x-mint.mcp.enabled: true` to root and all endpoint operations
4. Mintlify generates documentation with MCP enabled
5. The MCP server is automatically available at `https://[your-docs-url]/mcp`

## MCP Server Access

Once deployed, your MCP server will be available at:
- **URL**: `https://kintsugi.mintlify.app/mcp`
- You can find this URL in your Mintlify dashboard under the MCP Server section

**Note**: Mintlify only supports a single MCP server per documentation site. The merged OpenAPI file ensures all relevant endpoints are included in the single `/mcp` server.

## Security

- MCP servers only work with **public documentation** (not behind authentication)
- API endpoints exposed through MCP will use the authentication requirements defined in your OpenAPI `securitySchemes`
- Users will be prompted for authentication credentials when needed
- Only endpoints explicitly enabled for MCP are exposed

## Customization

To disable MCP for specific endpoints, you can add endpoint-level configuration:

```json
{
  "paths": {
    "/v1/admin/sensitive-endpoint": {
      "get": {
        "x-mint": {
          "mcp": {
            "enabled": false
          }
        }
      }
    }
  }
}
```

However, since we're using file-level configuration, all endpoints are enabled by default. If you need to exclude specific endpoints, you would need to modify the `create-merged-openapi.py` script to handle exclusions.

## Monitoring

You can monitor your MCP server and view all available tools in the Mintlify dashboard under the **MCP Server** section.

## References

- [Mintlify MCP Documentation](https://www.mintlify.com/docs/ai/model-context-protocol)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
