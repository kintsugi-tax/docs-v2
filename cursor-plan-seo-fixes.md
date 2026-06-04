# Cursor Plan — Docs Site SEO Errors + No-Index

This is a Mintlify v2 project (`docs.json` config). Fix the following 5 SEO errors and add
full crawler blocking. Do not touch content or navigation structure beyond what is specified.

---

## 1. Robots.txt — Fix Format Errors + Block All Crawlers (SE-62 related)

There is currently **no `robots.txt` in the project root**. Mintlify is auto-generating one
with format errors. Fix both problems at once:

**Create `/robots.txt` at the project root:**

```
User-agent: *
Disallow: /

Sitemap: https://docs.trykintsugi.com/sitemap.xml
```

This is a valid RFC-compliant robots.txt that blocks all crawlers and points to the sitemap.

---

## 2. Global Noindex Meta Tag — Block All Search Engine Indexing

In `docs.json`, add a top-level `metadata` block to inject `<meta name="robots">` on every page:

```json
"metadata": {
  "robots": "noindex, nofollow"
}
```

Place this at the top level of `docs.json` (same level as `"theme"`, `"name"`, etc.).

This complements the `robots.txt` — some crawlers respect one but not the other.

> **Note:** Also check the Mintlify dashboard under Settings → SEO for a "Prevent indexing"
> toggle, which may need to be enabled there as well.

---

## 3. Duplicate Title Tags — SE-60 (6 issues)

**Root cause:** Two API reference tabs — `"API Reference"` (`reference/api/…`) and
`"API Reference - Partners"` (`reference/partners/…`) — mirror ~35 identical endpoint
names. Mintlify generates `<title>` from the operation name, so both tabs produce
identical title tags.

In `docs.json`, add an `seo` block with a `titleTemplate` to each of the two affected tabs
to disambiguate them:

```json
{
  "tab": "API Reference",
  "seo": {
    "titleTemplate": "%s | Kintsugi API"
  },
  "pages": [...]
}
```

```json
{
  "tab": "API Reference - Partners",
  "seo": {
    "titleTemplate": "%s | Kintsugi Partners API"
  },
  "pages": [...]
}
```

> Check the Mintlify docs for the exact key name — it may be `titleSuffix` instead of
> `seo.titleTemplate` depending on the Mintlify version in use. Inspect `$schema` reference
> at `https://mintlify.com/docs.json` to confirm.

---

## 4. Duplicate Meta Descriptions — SE-61 (2 issues)

Same root cause as #3. The two most duplicated descriptions are the `estimate-tax` and
`create-transaction` endpoints which appear in both `reference/api/` and `reference/partners/`.

These are auto-generated from the OpenAPI spec `operationId` or `description` fields.
The fix is the same tab-level `seo` block from step 3 — once titles are disambiguated,
Mintlify uses the title in the meta description fallback, which will also de-duplicate them.

If the tool still flags 2 remaining pages after step 3, open `openapi.json` and
`openapi-partners.json` and ensure those two operations have distinct `description` values
at the operation level.

---

## 5. 3 Pages Returning 4XX Status Codes — SE-59

The `docs.json` already has redirects for `flashbacks`, `shopify-integration`,
`stripe-integration`, and `woocommerce-integration`. The remaining 4xx candidates are
orphan files that are accessible by direct URL but return errors when Mintlify can't
resolve them in navigation context.

**Fix:** Add these two missing redirects to the existing `"redirects"` array in `docs.json`:

```json
{
  "source": "/docs/rate-limiting",
  "destination": "/docs/error-handling"
},
{
  "source": "/docs/sdks/examples",
  "destination": "/docs/sdks/quick-start"
}
```

Also **delete** the following orphan files — they are no longer needed and can produce
stale crawl hits:
- `docs/flashbacks.mdx` (old "Kintsugi Sheets" product — wrong brand entirely)
- `docs/rate-limiting.mdx` (after adding redirect above)
- `docs/sdks/examples.mdx` (after adding redirect above)

> Do NOT delete `docs/woocommerce-integration.mdx`, `docs/stripe-integration.mdx`, or
> `docs/shopify-integration.mdx` yet — confirm redirects are live first.

---

## 6. Broken Internal Links — SE-63 related (11 found, 3 flagged by crawler)

The SEO tool flagged 3, but a full audit found **11 broken internal `href` targets**.
Fix all of them. Broken links are grouped by file:

### `docs/getting-started.mdx`
| Broken href | Fix |
|---|---|
| `/docs/troubleshooting` | Change to `/docs/error-handling` |
| `/docs/webhooks` | Remove the card/link entirely (no webhook docs exist) |
| `/docs/customers` | Change to `/reference/api/customers/get-customers` |
| `/docs/transactions` | Change to `/reference/api/transactions/get-transactions` |
| `/docs/registrations` | Change to `/reference/api/registrations/get-registrations` |

### `docs/api-guides/handling-refund-transactions.mdx`
| Broken href | Fix |
|---|---|
| `/reference/api/transactions/get-related-transactions` | Change to `/reference/api/transactions/get-transaction-by-id` |

### `docs/sdks/overview.mdx`
| Broken href | Fix |
|---|---|
| `/docs/sdks/customer-api` | Change to `/docs/sdks/overview` or remove card |
| `/docs/sdks/partners-api` | Change to `/docs/api-guides-partners/overview` |

### `docs/sdks/quick-start.mdx`
| Broken href | Fix |
|---|---|
| `/docs/sdks/error-handling` | Change to `/docs/error-handling` |
| `/docs/sdks/best-practices` | Change to `/docs/guides/integrating-kintsugis-api` |

### `docs/creating-and-managing-api-keys.mdx`
| Broken href | Fix |
|---|---|
| `/docs/integration-guides` | Change to `/docs/api-guides/planning-an-integration` |

---

## Summary Checklist

- [ ] Create `/robots.txt` with `Disallow: /`
- [ ] Add `"metadata": { "robots": "noindex, nofollow" }` to `docs.json`
- [ ] Add `seo.titleTemplate` (or `titleSuffix`) to both API Reference tabs in `docs.json`
- [ ] Add 2 missing redirects to `docs.json` redirects array (rate-limiting, sdks/examples)
- [ ] Delete `docs/flashbacks.mdx`, `docs/rate-limiting.mdx`, `docs/sdks/examples.mdx`
- [ ] Fix all 11 broken internal links across 5 files (see table above)
- [ ] Verify Mintlify dashboard Settings → SEO for any "Allow indexing" toggle to turn off
