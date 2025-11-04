#!/bin/bash

# Script to add MCP configuration to all endpoints in OpenAPI Partners spec
# This explicitly enables MCP for each endpoint
# Usage: ./scripts/add-mcp-config-to-endpoints.sh <openapi-file>

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

echo "🔧 Adding MCP configuration to all endpoints in $OPENAPI_FILE..."

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

# Add x-mint.mcp.enabled to each endpoint operation
# This ensures all endpoints are explicitly enabled for MCP
jq '
  # First ensure root-level x-mint exists
  . as $orig |
  if has("x-mint") then 
    ."x-mint"."mcp" = {"enabled": true}
  else 
    ."x-mint" = {"mcp": {"enabled": true}}
  end |
  
  # Then add x-mint.mcp.enabled to each endpoint operation
  .paths = (.paths | to_entries | map(
    .value = (.value | to_entries | map(
      if .key | test("^(get|post|put|patch|delete|options|head)$") then
        .value = (.value // {}) | 
        .value."x-mint" = ((.value."x-mint" // {}) + {"mcp": {"enabled": true}}) |
        .
      else
        .
      end
    ) | from_entries)
  ) | from_entries)
' "$OPENAPI_FILE" > "$TEMP_FILE"

# Replace the original file
mv "$TEMP_FILE" "$OPENAPI_FILE"

echo "✅ MCP configuration added to all endpoints!"
echo "📋 All endpoints are now explicitly enabled as MCP tools"

