# Docs Site Fixes — Unresolved Jira Tickets

The following issues were filed by Josh Hill (IT) against the Kintsugi docs site
(`docs.trykintsugi.com`) and have **not yet been resolved** by the recent overhaul.
Please address each one.

---

## SE-65 — Duplicate H1 Tags

**Root cause:** Mintlify auto-generates an `<h1>` from the frontmatter `title` field.
Any `# Heading` in the MDX body becomes a *second* H1 on the rendered page.

### Files to fix

**`docs/sdks/python.mdx`** — line 6 has `# Python SDK` which duplicates the frontmatter title.
Change it to `## Python SDK` **OR** delete it entirely (the frontmatter title already renders as H1).

**`docs/sdks/ruby.mdx`** — line 6 has `# Ruby SDK`. Same fix: downgrade to `##` or remove.

> The other bare `#` lines in those files (`# Initialize the client`, `# Calculate tax`, etc.)
> are **inside fenced code blocks** and are fine — don't touch them.

---

## SE-63 — Broken External Link to Old Support Docs

**File:** `docs/file-upload.mdx` (lines 14 and 16)

Both occurrences link to:
```
https://help.trykintsugi.com/en/articles/11146254-uploading-sales-transactions-via-csv-in-kintsugi
```

This is the "old support docs" external link flagged as broken. Options:
1. **Verify the URL is live** — if the Intercom/help article still exists, keep it.
2. **Replace with the correct URL** if the article was moved or deleted.
3. **Remove the external reference entirely** if the content has been migrated into this docs site.

---

## SE-60 / SE-61 — Duplicate Title Tags & Duplicate Meta Descriptions

**Root cause:** `docs.json` has two API reference tabs — `"API Reference"` (under `reference/api/`) and `"API Reference - Partners"` (under `reference/partners/`) — that mirror each other almost entirely. Mintlify generates page titles and meta descriptions from the page slug + OpenAPI operation names, so ~35+ pages end up with **identical `<title>` and `<meta name="description">` tags** across the two tabs.

Examples of duplicated slugs:
- `reference/api/tax-estimation/estimate-tax` ↔ `reference/partners/tax-estimation/estimate-tax`
- `reference/api/transactions/create-transaction` ↔ `reference/partners/transactions/create-transaction`
- (and ~30 more)

### How to fix

In Mintlify you can set `seo.title` and `seo.description` overrides per page group. In `docs.json`, add a `seo` block to each tab that disambiguates the titles:

```json
{
  "tab": "API Reference",
  "seo": {
    "titleTemplate": "%s — Kintsugi API"
  },
  "pages": [...]
}
```

```json
{
  "tab": "API Reference - Partners",
  "seo": {
    "titleTemplate": "%s — Kintsugi Partners API"
  },
  "pages": [...]
}
```

If Mintlify's current version supports `seo.titleTemplate` per tab, this resolves both SE-60 and SE-61 in one change. Check the Mintlify docs for the exact key name — it may be `titleSuffix` or similar.

Alternatively, if you want a bigger structural fix: consolidate the two tabs into one using
[Mintlify versioning or a conditional `x-internal` tag](https://mintlify.com/docs) so the same endpoint pages aren't duplicated under two paths.

---

## SE-59 — 4xx Pages (Orphaned / Missing Pages)

The navigation in `docs.json` appears complete — all listed pages have corresponding `.mdx` files.
However, there are **6 MDX files that exist but are not linked from navigation**, which could
account for old URLs that now return 404 or are unreachable:

| File | Note |
|------|------|
| `docs/flashbacks.mdx` | References "Kintsugi Sheets" — an old product. Should be **deleted** or redirected. If there's a live URL for this page, add a Mintlify redirect to a relevant current page. |
| `docs/rate-limiting.mdx` | Legitimate content, just missing from nav. Add it under the "Advanced" group in `docs.json`. |
| `docs/woocommerce-integration.mdx` | Integration page not in nav. Add to navigation or confirm it should be removed. |
| `docs/stripe-integration.mdx` | Same as above. |
| `docs/shopify-integration.mdx` | Same as above. |
| `docs/sdks/examples.mdx` | SDK examples, not linked from the SDK group in nav. Add under `docs/sdks/` group or merge content into `docs/sdks/quick-start.mdx`. |

### Adding redirects for removed/moved pages

If any of these files are being **deleted** (especially `flashbacks.mdx`), add a redirect in
`docs.json` so the old URL doesn't 404:

```json
"redirects": [
  {
    "source": "/docs/flashbacks",
    "destination": "/docs/getting-started"
  }
]
```

---

## SE-62 — Temporary Redirects Need Review

There is **no redirect configuration in `docs.json`**. Josh flagged that several temporary
redirects on the live site all point to the same destination despite having unrelated source URLs.

This is likely managed in the **Mintlify dashboard** (Settings → Redirects) rather than in code.
Action: log into the Mintlify dashboard and audit the redirect rules. Remove or update any
temporary redirects that are stale or pointing to incorrect destinations.

If you want to move redirect management into version control, add a `"redirects"` array to
`docs.json` and remove the dashboard-managed ones.

---

## Summary Checklist

- [ ] **SE-65** — Remove/downgrade `# Python SDK` in `docs/sdks/python.mdx` (line 6)
- [ ] **SE-65** — Remove/downgrade `# Ruby SDK` in `docs/sdks/ruby.mdx` (line 6)
- [ ] **SE-63** — Verify or fix the `help.trykintsugi.com` link in `docs/file-upload.mdx` (lines 14, 16)
- [ ] **SE-60/61** — Add `seo.titleTemplate` (or equivalent) to the two API reference tabs in `docs.json` to de-duplicate titles and meta descriptions
- [ ] **SE-59** — Delete `docs/flashbacks.mdx` (old product, wrong brand) + add redirect
- [ ] **SE-59** — Add `docs/rate-limiting` to navigation (Advanced group)
- [ ] **SE-59** — Decide fate of `docs/woocommerce-integration`, `docs/stripe-integration`, `docs/shopify-integration`, `docs/sdks/examples` — add to nav or delete + redirect
- [ ] **SE-62** — Audit redirects in Mintlify dashboard; move to `docs.json` if desired
