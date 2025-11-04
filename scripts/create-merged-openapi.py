#!/usr/bin/env python3
"""
Create a merged OpenAPI file combining Customer API + Public Partners API endpoints.

This script:
1. Loads Customer API spec (openapi.json)
2. Extracts public Partners API endpoints from docs.json ("API Reference - Partners")
3. Merges them into a single OpenAPI file for MCP
4. Adds MCP configuration to all endpoints
"""

import json
import re
import os
from pathlib import Path
from typing import Dict, Set, Tuple

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

def extract_openapi_paths_from_mdx(partners_pages: list, base_dir: str = 'reference/partners') -> Dict[Tuple[str, str], str]:
    """
    Extract OpenAPI paths from MDX files.
    Returns: {(method, path): mdx_file_path}
    """
    endpoint_map = {}
    
    for page in partners_pages:
        # Convert page path to file path
        mdx_file = f"{base_dir}/{page.replace('reference/partners/', '')}.mdx"
        
        if os.path.exists(mdx_file):
            with open(mdx_file, 'r') as f:
                content = f.read()
                # Extract openapi frontmatter: openapi: post /v1/transactions
                match = re.search(r'openapi:\s*(\w+)\s+([^\s]+)', content)
                if match:
                    method = match.group(1).lower()
                    path = match.group(2)
                    endpoint_map[(method, path)] = mdx_file
    
    return endpoint_map

def filter_partners_paths(full_partners_spec: dict, endpoint_map: Dict[Tuple[str, str], str]) -> dict:
    """
    Filter Partners OpenAPI spec to only include endpoints in endpoint_map.
    Returns just the paths dict.
    """
    filtered_paths = {}
    
    # Build set of paths to include
    paths_to_include = set()
    for (method, path) in endpoint_map.keys():
        paths_to_include.add(path)
    
    # Filter paths
    for path, methods in full_partners_spec.get('paths', {}).items():
        if path in paths_to_include:
            # Filter methods to only include those in our map
            filtered_methods = {}
            for method, spec in methods.items():
                if (method.lower(), path) in endpoint_map:
                    filtered_methods[method] = spec
            if filtered_methods:
                filtered_paths[path] = filtered_methods
    
    return filtered_paths

def merge_openapi_specs(customer_spec: dict, partners_paths: dict) -> dict:
    """
    Merge Customer API spec with filtered Partners API paths.
    Partners paths will override Customer paths if there's a conflict.
    """
    merged = customer_spec.copy()
    
    # Merge paths - Partners paths take precedence if there's a conflict
    merged_paths = merged.get('paths', {}).copy()
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
        merged['info']['title'] = merged['info'].get('title', 'Kintsugi API') + ' (Customer + Partners Public)'
        merged['info']['description'] = (merged['info'].get('description', '') + 
                                         '\n\nThis spec includes Customer API endpoints and public Partners API endpoints listed in "API Reference - Partners".').strip()
    
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
    print("🔍 Creating merged OpenAPI file (Customer API + Public Partners API)...")
    
    # Step 1: Load Customer API spec
    print("📥 Loading Customer API spec...")
    with open('openapi.json', 'r') as f:
        customer_spec = json.load(f)
    customer_path_count = len(customer_spec.get('paths', {}))
    print(f"✅ Loaded Customer API with {customer_path_count} paths")
    
    # Step 2: Get public Partners pages from docs.json
    print("📥 Extracting public Partners API pages from docs.json...")
    partners_pages = extract_partners_pages_from_docs('docs.json')
    print(f"✅ Found {len(partners_pages)} public Partners API pages")
    
    # Step 3: Extract OpenAPI paths from MDX files
    print("📥 Extracting OpenAPI paths from MDX files...")
    endpoint_map = extract_openapi_paths_from_mdx(partners_pages)
    print(f"✅ Mapped {len(endpoint_map)} Partners endpoints from MDX files")
    
    # Step 4: Load full Partners OpenAPI spec
    print("📥 Loading Partners API spec...")
    with open('openapi-partners.json', 'r') as f:
        partners_spec = json.load(f)
    partners_total_paths = len(partners_spec.get('paths', {}))
    print(f"✅ Loaded Partners API with {partners_total_paths} total paths")
    
    # Step 5: Filter Partners paths to only public ones
    print("🔍 Filtering Partners API to public endpoints only...")
    filtered_partners_paths = filter_partners_paths(partners_spec, endpoint_map)
    filtered_count = len(filtered_partners_paths)
    print(f"✅ Filtered to {filtered_count} public Partners endpoints")
    
    # Step 6: Merge Customer + filtered Partners
    print("🔀 Merging Customer API + Public Partners API...")
    merged_spec = merge_openapi_specs(customer_spec, filtered_partners_paths)
    merged_path_count = len(merged_spec.get('paths', {}))
    print(f"✅ Merged spec contains {merged_path_count} total paths")
    
    # Step 7: Add MCP configuration
    print("🔧 Adding MCP configuration...")
    merged_spec = add_mcp_config(merged_spec)
    print("✅ MCP configuration added to all endpoints")
    
    # Step 8: Save merged spec
    output_file = 'openapi.json'
    print(f"💾 Saving merged OpenAPI spec to {output_file}...")
    with open(output_file, 'w') as f:
        json.dump(merged_spec, f, indent=2)
    
    print(f"✅ Created merged OpenAPI spec: {output_file}")
    print(f"📋 Contains:")
    print(f"   - {customer_path_count} Customer API paths")
    print(f"   - {filtered_count} Public Partners API paths")
    print(f"   - {merged_path_count} total paths")
    print(f"   - All endpoints have MCP enabled")

if __name__ == '__main__':
    main()

