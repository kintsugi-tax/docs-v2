# Cursor prompt — Partner Experience auth & API-key docs update

> Copy everything below the line into Cursor (Composer / Agent mode) with the `docs-v2` repo open.

---

You are updating the **docs-v2** Mintlify documentation site (this repo). Production already shipped a refactor of how authentication and API keys work for the **Partner Experience (PX)**, and several guidance pages are now factually wrong. I've already run the deploy workflow, so the OpenAPI specs are current — **do not regenerate or hand-edit `openapi-customer.json` or `openapi-partners-public.json`, and do not touch anything under `reference/`** (those pages are auto-generated from the specs). This task is **prose/guidance content only**, plus nav/link sanity.

## What actually changed in production (source of truth)

1. **Partner API keys are now created and managed inside the Partner Experience itself**, under a **Settings** section. Partners no longer go into the main Kintsugi app (`app.trykintsugi.com`) to create an org-specific API key. Any doc that instructs a partner to log into the main app → Configuration → API Keys to mint an org key is now **incorrect**.
2. **Auth was refactored onto PropelAuth.** Partner orgs are now their own organizations in PropelAuth, separate from standard (client) orgs. As a result, a partner org is **provisioned automatically** — you no longer manually create a standalone org to associate with partner users.
3. **Partner-user invite emails now send automatically** when a user is added to the Partner Experience. The old multi-step workaround (create a Kintsugi user/account first, then invite into the PX) is going away.
4. The **programmatic** path is unchanged: `POST /v1/organizations/api_keys` still creates org-scoped keys for white-label/STaaS onboarding. Header auth is unchanged: `x-api-key` + `x-organization-id`.

> Net: the *programmatic* (API-driven) onboarding story stays the same; the *UI/manual* story for partners moves from the main app into the PX Settings area, and the partner login/invite flow is now PropelAuth-backed and automated.

## Files to update

**Primary (Stephen flagged these directly):**
- `docs/creating-and-managing-api-keys.mdx` — currently 100% the main-app flow (`app.trykintsugi.com` → **Configuration** → **API Keys**). Update so the **Partner Experience Settings → API Keys** flow is documented as the path for partners. Keep the main-app flow only where it's genuinely still correct for direct/customer accounts; if this page serves both audiences, split it into clearly labeled "Partner Experience" vs. "Kintsugi app (direct customers)" sections rather than overwriting one with the other.
- `docs/making-authenticate-request-using-api-key.mdx` — the "find your Organization ID in the lower-left of `app.trykintsugi.com`" instruction is wrong for partners; the org/client context and IDs come from within the PX now. Correct the location guidance for the partner audience while preserving the header examples (`x-api-key`, `x-organization-id`).

**Secondary (partner guides — reconcile the onboarding/auth narrative):**
- `docs/api-guides-partners/overview.mdx` — "Prerequisites" and the org-setup framing should reflect that partner orgs are PropelAuth-backed and that keys are managed in PX Settings; the programmatic `POST /v1/organizations/api_keys` flow stays.
- `docs/api-guides-partners/organization-setup.mdx` — Step 2 ("Create API Key") is fine programmatically; add a note that human/manual key management for a partner happens in **PX → Settings → API Keys**, not the main app. Make sure nothing here tells a partner to mint keys via the main app UI.

**Tertiary (link hygiene — only fix if the audience is partner-facing):**
- `docs/sdks/overview.mdx`, `docs/sdks/quick-start.mdx` — "retrieve your API key from the Kintsugi Platform (`app.trykintsugi.com`)" lines. For partner readers, point to PX Settings; for direct customers the main-app link is fine. Use judgment, don't blanket-replace.

## Guardrails

- **Do not invent UI labels, menu paths, or screenshots.** Use the exact section name as it appears in the PX. If you're unsure of the precise label ("Settings" vs. "Configuration", exact submenu wording), insert a clearly marked `{/* TODO: confirm exact PX label */}` comment rather than guessing.
- **Screenshots in `docs/creating-and-managing-api-keys.mdx` are from the main app and are now stale.** Don't fabricate replacements. Flag each stale `<Frame><img .../></Frame>` with a `{/* TODO: replace with PX Settings → API Keys screenshot */}` comment and keep the surrounding prose accurate.
- **Do not edit** `openapi-*.json` or anything in `reference/`. **Do not run** the docs/OpenAPI auto-update scripts.
- Preserve existing Mintlify component usage (`<Steps>`, `<Note>`, `<Warning>`, `<CardGroup>`, `<Frame>`) and frontmatter (including `noindex: true` where present).
- Keep header-auth facts intact: API key in `x-api-key`, org in `x-organization-id`, **not** bearer tokens.
- Check `docs.json` only to confirm no nav entries need renaming; don't restructure nav.

## When done

1. List every file you changed with a one-line summary of the change.
2. Run a search for any remaining instances of "main app" / `app.trykintsugi.com` / "Configuration" key-creation guidance that target partners, and report leftovers.
3. Note any `TODO` comments you left for me to resolve (exact PX labels, screenshots).
4. Do **not** commit or push — leave changes staged for my review.
