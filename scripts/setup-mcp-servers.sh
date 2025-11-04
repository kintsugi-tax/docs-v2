#!/bin/bash

# Script to set up three MCP servers:
# 1. /mcp-internal - All Partners API endpoints (openapi-partners.json)
# 2. /mcp-partners - Public Partners API endpoints only (openapi-partners-public.json)
# 3. /mcp-public - Customer API endpoints (openapi.json)

set -e

echo "🚀 Setting up MCP servers..."

# Install jq if needed
if ! command -v jq &> /dev/null; then
    echo "📦 Installing jq..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install jq
    else
        sudo apt-get update && sudo apt-get install -y jq
    fi
fi

# Install Python dependencies if needed
if ! python3 -c "import json" 2>/dev/null; then
    echo "❌ Python3 with json module required"
    exit 1
fi

# Step 1: Download Customer API spec
echo "📥 Downloading Customer API spec..."
curl -s https://api-doc.trykintsugi.com/openapi.json -o openapi.json

# Step 2: Add MCP configuration to Customer API (mcp-public)
echo "🔧 Adding MCP configuration to Customer API (mcp-public)..."
chmod +x scripts/add-mcp-config-to-endpoints.sh
./scripts/add-mcp-config-to-endpoints.sh openapi.json

# Step 3: Ensure Partners API has MCP configuration (mcp-internal)
echo "🔧 Ensuring Partners API has MCP configuration (mcp-internal)..."
if [ ! -f "openapi-partners.json" ]; then
    echo "📥 Downloading Partners API spec..."
    curl -s https://api.trykintsugi.com/openapi.json -o openapi-partners.json
fi
./scripts/add-mcp-config-to-endpoints.sh openapi-partners.json

# Step 4: Create filtered Partners API spec (mcp-partners)
echo "🔧 Creating filtered Partners API spec (mcp-partners)..."
chmod +x scripts/extract-public-partners-endpoints.py
python3 scripts/extract-public-partners-endpoints.py

echo "✅ MCP servers setup complete!"
echo ""
echo "📋 Generated files:"
echo "  - openapi.json (Customer API → /mcp-public)"
echo "  - openapi-partners.json (All Partners API → /mcp-internal)"
echo "  - openapi-partners-public.json (Public Partners API → /mcp-partners)"

