# 07 — Reuse search and duplication check

**Setup:** fixture with an existing `formatDate` helper and an existing `GET /orders` route used by the UI.

**Prompt:** `/A.plan show each order's created date on the dashboard in the user's locale`

**Pass when all hold:**
- [ ] The report's *Reuse candidates* names `formatDate` as exact or close, and the existing orders route as the data source; no new fetch path or new formatter is proposed.
- [ ] Any new literal (locale, format string, route) is placed in config or passed in, not hardcoded; the report says where.
- [ ] After implementation, Realign runs the duplication check and reports zero new duplicates, or names and removes them.
- [ ] Introduce a hardcoded route string during build (as the user): the `lean` lens or Realign flags it.
- [ ] `/A.simplify` after build cuts nothing that changes behaviour; each cut is followed by the check.
