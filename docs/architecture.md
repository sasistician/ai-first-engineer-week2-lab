# Ledger — Architecture Notes

_Last updated: launch, v0.1.0_

Ledger handles the order lifecycle for the checkout flow: create an order, charge the
customer, and refund if needed.

## Components

- `ledger.py` — `OrderService` (order lifecycle and state) and `PaymentClient` (talks to
  the external payment gateway).

## Scope (v1)

- Single full-amount charge per order.
- Full refunds only. Partial refunds are out of scope for v1.

## Stack

Python 3.11+, stdlib only. No external payment SDK yet — `PaymentClient` is a thin
wrapper we'll swap for the real gateway SDK post-launch.
