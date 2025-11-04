#!/bin/bash

# Script to add MCP configuration to OpenAPI Partners spec
# This enables MCP for all endpoints by default
# Usage: ./scripts/add-mcp-config.sh <openapi-file>

set -e

if [ -z "$1" ]; then
    echo "❌ Error: OpenAPI file path required"
    echo "Usage: $0 <openapi-file>"
    exit 1
fi

OPENAPI_FILE="$1"

if [ ! -f "$OPENAPI_FILE" ]; then
    echo "❌ Error: File not found: $OPENAPI_FILE"
    exit 1
fi

echo "🔧 Adding MCP configuration to $OPENAPI_FILE..."

# Check if jq is available
if ! command -v jq &> /dev/null; then
    echo "📦 Installing jq..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install jq
    else
        sudo apt-get update && sudo apt-get install -y jq
    fi
fi

# Create a temporary file
TEMP_FILE=$(mktemp)

# Add x-mint.mcp.enabled at the root level using jq
# This enables MCP for all endpoints by default
# Handle case where x-mint might already exist
jq 'if has("x-mint") then 
    ."x-mint"."mcp" = {"enabled": true} 
  else 
    . + {"x-mint": {"mcp": {"enabled": true}}}
  end' "$OPENAPI_FILE" > "$TEMP_FILE"

# Replace the original file
mv "$TEMP_FILE" "$OPENAPI_FILE"

echo "✅ MCP configuration added successfully!"
echo "📋 All endpoints in the Partners API will now be available as MCP tools"

