# MCP Server Troubleshooting

## Current Status

- ✅ OpenAPI Partners file has MCP configuration: `x-mint.mcp.enabled: true` at root level
- ✅ All 314 endpoint operations have explicit `x-mint.mcp.enabled: true` configuration
- ✅ Deployments show as successful in Mintlify dashboard
- ❌ MCP server at `https://kintsugi.mintlify.app/mcp` not showing all endpoints

## Potential Issues

### 1. Multiple OpenAPI Files

We have two OpenAPI files configured:
- `openapi.json` (Customer API) - 28 paths, **NO MCP configuration**
- `openapi-partners.json` (Partners API) - 274 paths, **HAS MCP configuration**

**Issue**: Mintlify might only be processing the first OpenAPI file listed in `docs.json`, or there might be a conflict when merging multiple files.

**Solution**: Add MCP configuration to the Customer API file as well, or verify Mintlify's behavior with multiple OpenAPI files.

### 2. MCP Server Cache

The MCP server might be cached and needs a manual refresh.

**Solution**: 
- Manually trigger a rebuild in Mintlify dashboard
- Wait for the next scheduled rebuild
- Clear browser cache and check again

### 3. MCP Server Generation Delay

MCP servers might regenerate on a different schedule than regular deployments.

**Solution**: Wait 10-15 minutes after deployment, then check again.

### 4. OpenAPI File Not Being Read

Mintlify might not be reading the updated `openapi-partners.json` file.

**Solution**: Verify the file is committed and pushed to the repository.

## Verification Steps

1. **Check if file is committed**:
   ```bash
   git log --oneline -1 -- openapi-partners.json
   ```

2. **Verify MCP configuration exists**:
   ```bash
   jq '."x-mint".mcp.enabled' openapi-partners.json
   # Should output: true
   
   jq '[.paths | to_entries[] | .value | to_entries[] | select(.key | test("^(get|post|put|patch|delete)$")) | .value."x-mint"."mcp"."enabled"] | unique' openapi-partners.json
   # Should output: [true]
   ```

3. **Check Mintlify Dashboard**:
   - Go to MCP Server section
   - Check "Available tools" - should list all Partners API endpoints
   - Review deployment logs for any errors

## Next Steps

1. **Add MCP to Customer API** (if needed):
   ```bash
   ./scripts/add-mcp-config-to-endpoints.sh openapi.json
   ```

2. **Manually trigger rebuild** in Mintlify dashboard

3. **Contact Mintlify Support** if issue persists:
   - Dashboard → Support
   - Or email: support@mintlify.com
   - Mention: MCP server not updating after successful deployment
   - Include: Link to your MCP server and OpenAPI file structure

## Reference

- [Mintlify MCP Documentation](https://www.mintlify.com/docs/ai/model-context-protocol)
- Deployment logs in Mintlify dashboard under "Activity"

