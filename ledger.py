"""Ledger — a small order/billing service.

Handles the order lifecycle: create an order, charge it, refund it.
Used as-is for the Week 2 lab. See ../week2-lab-guide.md.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass


@dataclass
class ChargeResult:
    charge_id: str
    amount_cents: int


class PaymentClient:
    """Talks to the (simulated) external payment gateway."""

    def __init__(self) -> None:
        self._seen_keys: dict[str, ChargeResult] = {}
        self._next_id = 1

    def charge(self, amount_cents: int, idempotency_key: str) -> ChargeResult:
        if idempotency_key in self._seen_keys:
            return self._seen_keys[idempotency_key]
        result = ChargeResult(charge_id=f"ch_{self._next_id:06d}", amount_cents=amount_cents)
        self._next_id += 1
        self._seen_keys[idempotency_key] = result
        return result

    def refund(self, charge_id: str, amount_cents: int) -> str:
        return f"re_{charge_id}"


@dataclass
class Order:
    order_id: str
    amount_cents: int
    status: str = "pending"
    charge_id: str | None = None


class OrderService:
    def __init__(self, payment_client: PaymentClient | None = None) -> None:
        self._payments = payment_client or PaymentClient()
        self._orders: dict[str, Order] = {}

    def create_order(self, amount_cents: int) -> Order:
        order = Order(order_id=f"ord_{uuid.uuid4().hex[:8]}", amount_cents=amount_cents)
        self._orders[order.order_id] = order
        return order

    def charge_order(self, order_id: str, idempotency_key: str) -> Order:
        order = self._orders[order_id]
        result = self._payments.charge(order.amount_cents, idempotency_key)
        order.charge_id = result.charge_id
        order.status = "paid"
        return order

    def refund_order(self, order_id: str, amount_cents: int | None = None) -> Order:
        order = self._orders[order_id]
        if amount_cents is not None and amount_cents < order.amount_cents:
            raise NotImplementedError(
                "Partial refunds aren't supported yet — see CHANGELOG.md."
            )
        self._payments.refund(order.charge_id, order.amount_cents)
        order.status = "refunded"
        return order
