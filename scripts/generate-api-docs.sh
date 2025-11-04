#!/bin/bash

# Script to generate API documentation from OpenAPI specs
# Usage: ./scripts/generate-api-docs.sh

set -e

echo "🚀 Generating API documentation from OpenAPI specs..."

# Create reference directories if they don't exist
mkdir -p reference/api reference/partners

# Setup all MCP servers first
echo "🔧 Setting up MCP servers..."
chmod +x scripts/setup-mcp-servers.sh
./scripts/setup-mcp-servers.sh

# Generate Customer API reference
echo "📥 Generating Customer API reference..."
npx @mintlify/scraping openapi-file openapi.json -o reference/api

# Generate Partners API reference (from full spec)
echo "📥 Generating Partners API reference..."
npx @mintlify/scraping openapi-file openapi-partners.json -o reference/partners

echo "✅ API documentation generated successfully!"
echo "📁 Customer API files created in: reference/api/"
echo "📁 Partners API files created in: reference/partners/"
echo "🔗 Both API references are configured in docs.json"

# List generated files
echo "📋 Customer API files:"
find reference/api -name "*.mdx" | head -5
echo "... (and more)"

echo "📋 Partners API files:"
find reference/partners -name "*.mdx" | head -5
echo "... (and more)"

echo "🎉 Done! Both API references are ready."
