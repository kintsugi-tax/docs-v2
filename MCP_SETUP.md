# MCP (Model Context Protocol) Setup

This document explains how MCP is configured for the Kintsugi Partners API documentation.

## Overview

The Model Context Protocol (MCP) enables AI tools (like Claude, Cursor, VS Code) to access your documentation and API endpoints. Our setup automatically enables MCP for all endpoints in the Partners API reference.

## Configuration

MCP is configured at the file level in the `openapi-partners.json` file using the `x-mint` extension:

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

This enables MCP for **all endpoints** in the Partners API by default. New endpoints that are added to the API will automatically be available as MCP tools once the OpenAPI spec is updated.

## Automatic Updates

The MCP configuration is automatically applied in two places:

1. **GitHub Actions Workflow** (`.github/workflows/update-api-docs.yml`):
   - Runs every 6 hours
   - Downloads the latest OpenAPI spec from `https://api.trykintsugi.com/openapi.json`
   - Automatically adds MCP configuration
   - Regenerates documentation
   - Commits changes if updates are detected

2. **Local Script** (`scripts/generate-api-docs.sh`):
   - Can be run manually for local development
   - Uses `scripts/add-mcp-config.sh` to add MCP configuration

## How It Works

When the OpenAPI spec is downloaded:
1. The spec is fetched from the API endpoint
2. The `add-mcp-config.sh` script adds the `x-mint.mcp.enabled: true` configuration
3. Mintlify generates documentation with MCP enabled
4. The MCP server is automatically available at `https://[your-docs-url]/mcp`

## MCP Server Access

Once deployed, your MCP server will be available at:
- **URL**: `https://[your-mintlify-docs-url]/mcp`
- You can find this URL in your Mintlify dashboard under the MCP Server section

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

However, since we're using file-level configuration, all endpoints are enabled by default. If you need to exclude specific endpoints, you would need to modify the script to handle exclusions.

## Monitoring

You can monitor your MCP server and view all available tools in the Mintlify dashboard under the **MCP Server** section.

## References

- [Mintlify MCP Documentation](https://www.mintlify.com/docs/ai/model-context-protocol)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)

