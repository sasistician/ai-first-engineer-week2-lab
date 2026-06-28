# Changelog

## v0.4.0 — 2024-03-12
- `PaymentClient.charge()` now requires an `idempotency_key`. Added after a production
  incident: a retried request without one caused a customer to be charged twice for the
  same order. Callers must reuse the same key when retrying the same logical charge —
  a fresh key per retry defeats the protection entirely.

## v0.3.0 — 2024-01-05
- Decided **not** to support partial refunds in v1. Full refunds only for now — revisit
  after the v2 ledger-reconciliation rework. This needs product sign-off, not just an
  engineering fix, so don't build it just because a customer asked.

## v0.1.0 — 2023-09-01
- Initial release: order creation, full payment charge, full refund.
