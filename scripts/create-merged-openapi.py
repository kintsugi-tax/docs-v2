#!/usr/bin/env python3
"""
Create OpenAPI file for MCP from endpoints explicitly listed in "API Reference - Partners".

This script:
1. Extracts endpoints from docs.json ("API Reference - Partners" tab)
2. Maps endpoints to either Customer API or Partners API specs
3. Filters both API specs to only include publicly documented endpoints
4. Merges them into a single OpenAPI file for MCP
5. Adds MCP configuration to all endpoints

The "API Reference - Partners" tab includes all Customer API endpoints plus additional
Partners endpoints that should be available via MCP.
"""

import json
import re
import os
from typing import Dict, Tuple

def extract_partners_pages_from_docs(docs_file: str) -> list:
    """Extract all Partners API reference pages from docs.json."""
    with open(docs_file, 'r') as f:
        docs = json.load(f)
    
    partners_pages = []
    for version in docs['navigation']['versions']:
        for tab in version.get('tabs', []):
            if tab.get('tab') == 'API Reference - Partners':
                for group in tab.get('pages', []):
                    if isinstance(group, dict) and 'pages' in group:
                        partners_pages.extend(group['pages'])
    
    return partners_pages

def extract_openapi_paths_from_mdx(pages: list) -> Dict[Tuple[str, str], Tuple[str, str]]:
    """
    Extract OpenAPI paths from MDX files.
    Returns: {(method, path): (source_spec, mdx_file_path)}
    source_spec is either 'customer' or 'partners'
    """
    endpoint_map = {}
    
    for page in pages:
        # All pages in "API Reference - Partners" are in reference/partners/
        if not page.startswith('reference/partners/'):
            continue
            
        mdx_file = f"{page}.mdx"
        
        if os.path.exists(mdx_file):
            with open(mdx_file, 'r') as f:
                content = f.read()
                # Extract openapi frontmatter: openapi: post /v1/transactions
                match = re.search(r'openapi:\s*(\w+)\s+([^\s]+)', content)
                if match:
                    method = match.group(1).lower()
                    path = match.group(2)
                    # Determine source spec - check if endpoint exists in Customer API
                    # For now, we'll check both specs when filtering
                    endpoint_map[(method, path)] = ('both', mdx_file)
    
    return endpoint_map

def filter_api_paths(full_spec: dict, endpoint_map: Dict[Tuple[str, str], Tuple[str, str]]) -> dict:
    """
    Filter OpenAPI spec to only include endpoints in endpoint_map.
    Returns just the paths dict.
    """
    filtered_paths = {}
    
    # Filter paths
    for path, methods in full_spec.get('paths', {}).items():
        # Filter methods to only include those in our map
        filtered_methods = {}
        for method, spec in methods.items():
            if (method.lower(), path) in endpoint_map:
                filtered_methods[method] = spec
        if filtered_methods:
            filtered_paths[path] = filtered_methods
    
    return filtered_paths

def merge_openapi_specs(customer_paths: dict, partners_paths: dict, base_spec: dict) -> dict:
    """
    Merge filtered Customer API paths with filtered Partners API paths.
    Partners paths will override Customer paths if there's a conflict.
    Uses base_spec for schema definitions and other non-path content.
    """
    merged = base_spec.copy()
    
    # Start with Customer paths
    merged_paths = customer_paths.copy()
    
    # Merge Partners paths - Partners paths take precedence if there's a conflict
    for path, methods in partners_paths.items():
        if path in merged_paths:
            # Merge methods - Partners methods take precedence
            merged_methods = merged_paths[path].copy()
            merged_methods.update(methods)
            merged_paths[path] = merged_methods
        else:
            merged_paths[path] = methods
    
    merged['paths'] = merged_paths
    
    # Update info
    if 'info' in merged:
        merged['info']['title'] = merged['info'].get('title', 'Kintsugi API') + ' (Public API Reference)'
        merged['info']['description'] = (merged['info'].get('description', '') + 
                                         '\n\nThis spec includes only publicly documented endpoints from the Customer API ("API Reference") and Partners API ("API Reference - Partners").').strip()
    
    return merged

def add_mcp_config(spec: dict) -> dict:
    """Add MCP configuration to root and all endpoints."""
    # Root level MCP config
    spec['x-mint'] = {
        'mcp': {
            'enabled': True
        }
    }
    
    # Add MCP config to each endpoint operation
    for path, methods in spec.get('paths', {}).items():
        for method, operation in methods.items():
            if isinstance(operation, dict) and method.lower() in ['get', 'post', 'put', 'patch', 'delete', 'options', 'head']:
                if 'x-mint' not in operation:
                    operation['x-mint'] = {}
                operation['x-mint']['mcp'] = {'enabled': True}
    
    return spec

def main():
    print("🔍 Creating OpenAPI file for MCP from 'API Reference - Partners' endpoints...")
    
    # Step 1: Get public Partners API pages from docs.json
    # This tab includes all Customer API endpoints + additional Partners endpoints
    print("📥 Extracting endpoints from 'API Reference - Partners' tab in docs.json...")
    partners_pages = extract_partners_pages_from_docs('docs.json')
    print(f"✅ Found {len(partners_pages)} endpoints in 'API Reference - Partners'")
    
    # Step 2: Extract OpenAPI paths from MDX files
    print("📥 Extracting OpenAPI paths from MDX files...")
    endpoint_map = extract_openapi_paths_from_mdx(partners_pages)
    print(f"✅ Mapped {len(endpoint_map)} endpoints from MDX files")
    
    # Step 3: Load full Customer API spec
    print("📥 Loading Customer API spec...")
    with open('openapi-customer.json', 'r') as f:
        customer_spec = json.load(f)
    customer_total_paths = len(customer_spec.get('paths', {}))
    print(f"✅ Loaded Customer API with {customer_total_paths} total paths")
    
    # Step 4: Load full Partners OpenAPI spec
    print("📥 Loading Partners API spec...")
    with open('openapi-partners.json', 'r') as f:
        partners_spec = json.load(f)
    partners_total_paths = len(partners_spec.get('paths', {}))
    print(f"✅ Loaded Partners API with {partners_total_paths} total paths")
    
    # Step 5: Filter Customer API paths to only endpoints in "API Reference - Partners"
    print("🔍 Filtering Customer API to endpoints in 'API Reference - Partners'...")
    filtered_customer_paths = filter_api_paths(customer_spec, endpoint_map)
    filtered_customer_count = len(filtered_customer_paths)
    print(f"✅ Filtered to {filtered_customer_count} Customer API endpoints")
    
    # Step 6: Filter Partners paths to only endpoints in "API Reference - Partners"
    print("🔍 Filtering Partners API to endpoints in 'API Reference - Partners'...")
    filtered_partners_paths = filter_api_paths(partners_spec, endpoint_map)
    filtered_partners_count = len(filtered_partners_paths)
    print(f"✅ Filtered to {filtered_partners_count} Partners API endpoints")
    
    # Step 7: Merge filtered Customer + filtered Partners
    # Use Customer spec as base (it likely has more complete schemas)
    print("🔀 Merging filtered Customer API + filtered Partners API...")
    merged_spec = merge_openapi_specs(filtered_customer_paths, filtered_partners_paths, customer_spec)
    merged_path_count = len(merged_spec.get('paths', {}))
    print(f"✅ Merged spec contains {merged_path_count} total paths")
    
    # Step 8: Add MCP configuration
    print("🔧 Adding MCP configuration...")
    merged_spec = add_mcp_config(merged_spec)
    print("✅ MCP configuration added to all endpoints")
    
    # Step 9: Save merged spec
    output_file = 'openapi.json'
    print(f"💾 Saving OpenAPI spec to {output_file}...")
    with open(output_file, 'w') as f:
        json.dump(merged_spec, f, indent=2)
    
    print(f"✅ Created OpenAPI spec for MCP: {output_file}")
    print("📋 Contains:")
    print(f"   - {filtered_customer_count} Customer API endpoints from 'API Reference - Partners'")
    print(f"   - {filtered_partners_count} Partners API endpoints from 'API Reference - Partners'")
    print(f"   - {merged_path_count} total paths")
    print("   - All endpoints have MCP enabled")

if __name__ == '__main__':
    main()

