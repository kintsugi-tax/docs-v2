#!/bin/bash

# Local mirror of the CI pipeline in .github/workflows/update-api-docs.yml.
# Builds the public Partner spec and regenerates the Customer API reference pages.
#
# Usage: ./scripts/generate-api-docs.sh
#   Expects openapi-customer.json and openapi-partners.json to be present
#   (download them from https://api-doc.trykintsugi.com/openapi.json and
#    https://api.trykintsugi.com/openapi.json respectively).

set -e

if [ ! -f "openapi-partners.json" ] || [ ! -f "openapi-customer.json" ]; then
  echo "Missing source specs. Download them first:"
  echo "  curl -fsSL -o openapi-customer.json https://api-doc.trykintsugi.com/openapi.json"
  echo "  curl -fsSL -o openapi-partners.json https://api.trykintsugi.com/openapi.json"
  exit 1
fi

echo "Building public Partner API spec (openapi-partners-public.json)..."
python3 scripts/build-public-openapi.py

echo "Regenerating Customer API reference pages..."
mkdir -p reference/api
npx @mintlify/scraping openapi-file openapi-customer.json -o reference/api

echo "Done."
echo "  - openapi-partners-public.json powers the 'API Reference - Partners' tab"
echo "  - reference/api/ powers the 'API Reference' tab"
