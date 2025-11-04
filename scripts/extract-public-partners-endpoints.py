#!/usr/bin/env python3
"""
Extract public Partners API endpoints from docs.json and create a filtered OpenAPI spec.

This script:
1. Reads docs.json to find all endpoints listed in "API Reference - Partners"
2. Reads openapi-partners.json to get the full spec
3. Extracts OpenAPI paths from MDX files to map pages to endpoints
4. Creates a filtered OpenAPI spec with only public endpoints
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

def filter_openapi_spec(full_spec: dict, endpoint_map: Dict[Tuple[str, str], str]) -> dict:
    """
    Filter OpenAPI spec to only include endpoints in endpoint_map.
    """
    filtered_spec = full_spec.copy()
    filtered_paths = {}
    
    # Build set of paths to include
    paths_to_include = set()
    for (method, path) in endpoint_map.keys():
        paths_to_include.add(path)
    
    # Filter paths
    for path, methods in full_spec.get('paths', {}).items():
        if path in paths_to_include:
            # Filter methods to only include those in our map
            filtered_methods = {}
            for method, spec in methods.items():
                if (method.lower(), path) in endpoint_map:
                    filtered_methods[method] = spec
            if filtered_methods:
                filtered_paths[path] = filtered_methods
    
    filtered_spec['paths'] = filtered_paths
    
    # Update info
    if 'info' in filtered_spec:
        filtered_spec['info']['title'] = filtered_spec['info'].get('title', 'Tax Platform') + ' - Partners (Public)'
        filtered_spec['info']['description'] = 'Public Partners API endpoints only'
    
    return filtered_spec

def main():
    print("🔍 Extracting public Partners API endpoints...")
    
    # Step 1: Get public pages from docs.json
    partners_pages = extract_partners_pages_from_docs('docs.json')
    print(f"✅ Found {len(partners_pages)} public Partners API pages in docs.json")
    
    # Step 2: Extract OpenAPI paths from MDX files
    endpoint_map = extract_openapi_paths_from_mdx(partners_pages)
    print(f"✅ Mapped {len(endpoint_map)} endpoints from MDX files")
    
    # Step 3: Load full Partners OpenAPI spec
    with open('openapi-partners.json', 'r') as f:
        full_spec = json.load(f)
    
    print(f"✅ Loaded full Partners API spec with {len(full_spec.get('paths', {}))} paths")
    
    # Step 4: Filter the spec
    filtered_spec = filter_openapi_spec(full_spec, endpoint_map)
    
    filtered_path_count = len(filtered_spec.get('paths', {}))
    print(f"✅ Filtered spec contains {filtered_path_count} paths")
    
    # Step 5: Add MCP configuration
    filtered_spec['x-mint'] = {
        'mcp': {
            'enabled': True
        }
    }
    
    # Add MCP to each endpoint
    for path, methods in filtered_spec.get('paths', {}).items():
        for method, spec in methods.items():
            if isinstance(spec, dict):
                if 'x-mint' not in spec:
                    spec['x-mint'] = {}
                spec['x-mint']['mcp'] = {'enabled': True}
    
    # Step 6: Save filtered spec
    output_file = 'openapi-partners-public.json'
    with open(output_file, 'w') as f:
        json.dump(filtered_spec, f, indent=2)
    
    print(f"✅ Created filtered OpenAPI spec: {output_file}")
    print(f"📋 Contains {filtered_path_count} public endpoints")

if __name__ == '__main__':
    main()

