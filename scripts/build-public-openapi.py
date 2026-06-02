#!/usr/bin/env python3
"""
Build the public Partner OpenAPI spec used by the "API Reference - Partners" tab.

Pipeline (driven entirely by docs.json so the published surface stays in sync
with the navigation that humans actually curate):

1. Read the pages listed under the "API Reference - Partners" tab in docs.json.
2. Read each page's `openapi: METHOD /path` frontmatter to get the documented
   endpoint set.
3. Filter the full partner spec (openapi-partners.json) down to exactly that set.
4. Version handling: documented paths are pinned to /v1. If a documented /v1 path
   is missing from the source spec but its /v2 sibling exists, the operation is
   pulled from /v2 and re-keyed under the documented /v1 path (and vice versa).
   Every rewrite is logged. If neither version exists, the build FAILS LOUDLY so
   a future backend version bump can never silently produce an empty page.
5. Inject a `servers` block (the source partner spec ships without one).
6. Enable Mintlify MCP (`x-mint.mcp`) at the root and on every operation.

Output: openapi-partners-public.json (override with OUTPUT_FILE).

Inputs:
  docs.json
  openapi-partners.json   (full partner spec, downloaded in CI)
"""

import json
import os
import re
from typing import Dict, List, Optional, Set, Tuple

DOCS_FILE = "docs.json"
PARTNERS_SPEC_FILE = "openapi-partners.json"
PARTNERS_TAB = "API Reference - Partners"
DEFAULT_OUTPUT = "openapi-partners-public.json"
SERVER_URL = "https://api.trykintsugi.com"

Endpoint = Tuple[str, str]  # (method, path)

VERSION_RE = re.compile(r"^/v(\d+)/")


def _collect_page_slugs(node, out: List[str]) -> None:
    """Recursively collect string page slugs from a navigation subtree,
    descending through arbitrarily nested groups."""
    if isinstance(node, str):
        out.append(node)
    elif isinstance(node, list):
        for item in node:
            _collect_page_slugs(item, out)
    elif isinstance(node, dict):
        _collect_page_slugs(node.get("pages", []), out)


def collect_partner_page_paths(docs: dict) -> List[str]:
    """Return every page slug listed under the Partners API Reference tab."""
    pages: List[str] = []
    for version in docs.get("navigation", {}).get("versions", []):
        for tab in version.get("tabs", []):
            if tab.get("tab") != PARTNERS_TAB:
                continue
            _collect_page_slugs(tab.get("pages", []), pages)
    return pages


def documented_endpoints(page_slugs: List[str]) -> Set[Endpoint]:
    """Read `openapi: METHOD /path` frontmatter from each referenced MDX page."""
    endpoints: Set[Endpoint] = set()
    missing_files: List[str] = []
    for slug in page_slugs:
        mdx = f"{slug}.mdx"
        if not os.path.exists(mdx):
            missing_files.append(mdx)
            continue
        with open(mdx, "r") as fh:
            match = re.search(r"openapi:\s*(\w+)\s+(\S+)", fh.read())
        if match:
            endpoints.add((match.group(1).lower(), match.group(2)))
    if missing_files:
        print("⚠️  Navigation references MDX files that do not exist:")
        for mdx in missing_files:
            print(f"     - {mdx}")
        raise SystemExit(1)
    return endpoints


def alternate_version(path: str) -> Optional[str]:
    """Return the sibling path with the version segment flipped (v1<->v2)."""
    match = VERSION_RE.match(path)
    if not match:
        return None
    current = int(match.group(1))
    alt = 1 if current != 1 else 2
    return VERSION_RE.sub(f"/v{alt}/", path, count=1)


def resolve_operation(source_paths: dict, method: str, path: str,
                      rewrites: List[str]) -> Optional[dict]:
    """Return the operation for (method, path), falling back to the sibling
    version and logging the rewrite. Returns None if neither version exists."""
    operation = source_paths.get(path, {}).get(method)
    if operation is not None:
        return operation

    alt = alternate_version(path)
    alt_op = source_paths.get(alt, {}).get(method) if alt else None
    if alt_op is not None:
        rewrites.append(f"{method.upper()} {alt} -> documented as {path}")
        return alt_op

    return None


def build_public_spec(spec: dict, endpoints: Set[Endpoint]) -> dict:
    """Filter `spec` to `endpoints`, applying version-fallback rewriting."""
    source_paths = spec.get("paths", {})
    public_paths: Dict[str, dict] = {}
    rewrites: List[str] = []
    unresolved: List[str] = []

    for method, path in sorted(endpoints):
        operation = resolve_operation(source_paths, method, path, rewrites)
        if operation is None:
            unresolved.append(f"{method.upper()} {path}")
            continue
        public_paths.setdefault(path, {})[method] = operation

    if rewrites:
        print("ℹ️  Version rewrites applied (source -> documented):")
        for line in rewrites:
            print(f"     - {line}")

    if unresolved:
        print("❌ Documented endpoints not found in the source partner spec "
              "(checked both /v1 and /v2):")
        for line in unresolved:
            print(f"     - {line}")
        print("   Fix the navigation/frontmatter or update the source spec. "
              "Refusing to build a spec with missing endpoints.")
        raise SystemExit(1)

    public = dict(spec)
    public["paths"] = public_paths
    public["servers"] = [{"url": SERVER_URL, "description": "Production API server"}]
    enforce_api_key_auth(public)

    info = dict(public.get("info", {}))
    info["title"] = "Kintsugi Partner API"
    info["description"] = (
        "Publicly documented Kintsugi Partner API endpoints. Generated from the "
        "\"API Reference - Partners\" navigation in docs.json."
    )
    public["info"] = info

    return enable_mcp(public)


API_KEY_SCHEME = "APIKeyHeader"
INTERNAL_AUTH_SCHEMES = {"HTTPBearer"}


def enforce_api_key_auth(spec: dict) -> None:
    """Strip internal-only (bearer) auth so the public playground only offers
    the X-API-KEY scheme. Bearer-authenticated access is internal per policy."""
    http_methods = {"get", "post", "put", "patch", "delete", "options", "head"}
    for methods in spec.get("paths", {}).values():
        for method, operation in methods.items():
            if method.lower() not in http_methods or not isinstance(operation, dict):
                continue
            if "security" not in operation:
                continue
            kept = [
                requirement
                for requirement in operation["security"]
                if not (set(requirement) & INTERNAL_AUTH_SCHEMES)
            ]
            operation["security"] = kept or [{API_KEY_SCHEME: []}]

    schemes = spec.get("components", {}).get("securitySchemes", {})
    for name in INTERNAL_AUTH_SCHEMES:
        schemes.pop(name, None)

    spec["security"] = [{API_KEY_SCHEME: []}]


def enable_mcp(spec: dict) -> dict:
    """Enable Mintlify MCP at the root and on every operation."""
    spec["x-mint"] = {"mcp": {"enabled": True}}
    http_methods = {"get", "post", "put", "patch", "delete", "options", "head"}
    for methods in spec.get("paths", {}).values():
        for method, operation in methods.items():
            if method.lower() in http_methods and isinstance(operation, dict):
                operation.setdefault("x-mint", {})["mcp"] = {"enabled": True}
    return spec


def main() -> None:
    print("🔧 Building public Partner OpenAPI spec...")

    with open(DOCS_FILE, "r") as fh:
        docs = json.load(fh)
    page_slugs = collect_partner_page_paths(docs)
    print(f"✅ Found {len(page_slugs)} pages under '{PARTNERS_TAB}'")

    endpoints = documented_endpoints(page_slugs)
    print(f"✅ Resolved {len(endpoints)} documented endpoints from frontmatter")

    with open(PARTNERS_SPEC_FILE, "r") as fh:
        partner_spec = json.load(fh)
    print(f"✅ Loaded source partner spec with "
          f"{len(partner_spec.get('paths', {}))} paths")

    public_spec = build_public_spec(partner_spec, endpoints)
    print(f"✅ Public spec contains {len(public_spec['paths'])} paths "
          "with MCP enabled")

    output_file = os.environ.get("OUTPUT_FILE", DEFAULT_OUTPUT)
    with open(output_file, "w") as fh:
        json.dump(public_spec, fh, indent=2)
    print(f"💾 Wrote {output_file}")


if __name__ == "__main__":
    main()
