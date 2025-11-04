#!/bin/bash

# Script to generate API documentation from OpenAPI specs
# Usage: ./scripts/generate-api-docs.sh

set -e

echo "🚀 Generating API documentation from OpenAPI specs..."

# Create reference directories if they don't exist
mkdir -p reference/api reference/partners

# Generate Customer API reference
echo "📥 Fetching Customer API spec from https://api-doc.trykintsugi.com/openapi.json..."
npx @mintlify/scraping openapi-file https://api-doc.trykintsugi.com/openapi.json -o reference/api

# Generate Partners API reference
echo "📥 Fetching Partners API spec from https://api.trykintsugi.com/openapi.json..."
curl -o openapi-partners-temp.json https://api.trykintsugi.com/openapi.json

# Add MCP configuration to Partners API
echo "🔧 Adding MCP configuration to Partners API spec..."
./scripts/add-mcp-config.sh openapi-partners-temp.json

# Generate documentation from the MCP-enabled spec
npx @mintlify/scraping openapi-file openapi-partners-temp.json -o reference/partners

# Move the configured spec to the final location
mv openapi-partners-temp.json openapi-partners.json

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
