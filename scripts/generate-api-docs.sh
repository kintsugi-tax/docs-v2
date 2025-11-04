#!/bin/bash

# Script to generate API documentation from merged OpenAPI spec
# Usage: ./scripts/generate-api-docs.sh

set -e

echo "🚀 Generating API documentation from merged OpenAPI spec..."

# Create reference directories if they don't exist
mkdir -p reference/api

# Ensure merged OpenAPI file exists
if [ ! -f "openapi.json" ]; then
    echo "❌ Error: openapi.json not found"
    echo "Please run create-merged-openapi.py first or ensure the file exists"
    exit 1
fi

# Generate API reference from merged spec
echo "📥 Generating API reference documentation..."
npx @mintlify/scraping openapi-file openapi.json -o reference/api

echo "✅ API documentation generated successfully!"
echo "📁 API reference files created in: reference/api/"
echo "🔗 Merged OpenAPI file includes Customer API + Public Partners API endpoints"

# List generated files
echo "📋 Generated API reference files:"
find reference/api -name "*.mdx" | head -10
echo "... (and more)"

echo "🎉 Done! API reference documentation is ready."
