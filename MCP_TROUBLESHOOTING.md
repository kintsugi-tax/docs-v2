# MCP Server Troubleshooting

## Current Status

- ✅ Merged OpenAPI file has MCP configuration: `x-mint.mcp.enabled: true` at root level
- ✅ All endpoint operations have explicit `x-mint.mcp.enabled: true` configuration
- ✅ Merged file includes Customer API + Public Partners API endpoints
- ✅ Single MCP server at `/mcp` path

## Verification Steps

1. **Check if merged OpenAPI file exists and has MCP enabled**:
   ```bash
   jq '."x-mint".mcp.enabled' openapi.json
   # Should output: true
   ```

2. **Verify endpoint-level MCP configuration**:
   ```bash
   jq '[.paths | to_entries[] | .value | to_entries[] | select(.key | test("^(get|post|put|patch|delete)$")) | .value."x-mint"."mcp"."enabled"] | unique' openapi.json
   # Should output: [true]
   ```

3. **Count total paths in merged file**:
   ```bash
   jq '.paths | length' openapi.json
   ```

4. **Check Mintlify Dashboard**:
   - Go to MCP Server section
   - Check "Available tools" - should list all Customer API + Public Partners API endpoints
   - Review deployment logs for any errors

## Common Issues

### 1. MCP Server Not Showing All Endpoints

**Symptoms**: MCP server at `/mcp` shows fewer endpoints than expected

**Possible Causes**:
- Partners API endpoints not included in "API Reference - Partners" section
- MDX files missing `openapi:` frontmatter
- Merge script not including all intended endpoints

**Solution**:
- Verify all intended Partners endpoints are listed in `docs.json` under "API Reference - Partners"
- Check that MDX files have correct `openapi: {method} {path}` frontmatter
- Run `create-merged-openapi.py` script locally to verify merge logic
- Check GitHub Actions logs for merge script output

### 2. MCP Server Cache

The MCP server might be cached and needs a manual refresh.

**Solution**: 
- Manually trigger a rebuild in Mintlify dashboard
- Wait for the next scheduled rebuild (every 6 hours)
- Clear browser cache and check again

### 3. MCP Server Generation Delay

MCP servers might regenerate on a different schedule than regular deployments.

**Solution**: Wait 10-15 minutes after deployment, then check again.

### 4. Partners Endpoints Missing

If Partners API endpoints are missing from the MCP server:

**Check**:
1. Verify endpoint is listed in `docs.json` under "API Reference - Partners"
2. Verify MDX file exists: `reference/partners/{category}/{endpoint}.mdx`
3. Check MDX frontmatter: Should have `openapi: {method} {path}`
4. Run merge script locally to verify endpoint is included

**Solution**:
- Add missing endpoint to "API Reference - Partners" section in `docs.json`
- Create MDX file with correct frontmatter
- Re-run `create-merged-openapi.py` script

### 5. Customer API Endpoints Missing

If Customer API endpoints are missing:

**Check**:
1. Verify Customer API spec downloaded correctly
2. Check GitHub Actions logs for download errors
3. Verify `openapi-customer.json` contains expected endpoints

**Solution**:
- Manually trigger GitHub Actions workflow
- Check Customer API endpoint: `https://api-doc.trykintsugi.com/openapi.json`

## Manual Testing

To test the merge locally:

```bash
# 1. Download specs
curl -o openapi-customer.json https://api-doc.trykintsugi.com/openapi.json
curl -o openapi-partners.json https://api.trykintsugi.com/openapi.json

# 2. Copy Customer API to openapi.json (script expects it)
cp openapi-customer.json openapi.json

# 3. Run merge script
python3 scripts/create-merged-openapi.py

# 4. Verify merged file
jq '.paths | length' openapi.json
jq '."x-mint".mcp.enabled' openapi.json
```

## Next Steps

1. **Check GitHub Actions logs** - Verify merge script ran successfully
2. **Manually trigger rebuild** in Mintlify dashboard
3. **Verify MCP server** - Check `/mcp` endpoint for all expected tools
4. **Contact Mintlify Support** if issue persists:
   - Dashboard → Support
   - Mention: Single MCP server with merged OpenAPI file
   - Include: Link to your MCP server and OpenAPI file structure

## Reference

- [Mintlify MCP Documentation](https://www.mintlify.com/docs/ai/model-context-protocol)
- Deployment logs in Mintlify dashboard under "Activity"
- GitHub Actions logs in repository → Actions
