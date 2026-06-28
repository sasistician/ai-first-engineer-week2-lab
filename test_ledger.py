from ledger import OrderService


def test_create_and_charge_order():
    svc = OrderService()
    order = svc.create_order(amount_cents=2000)
    charged = svc.charge_order(order.order_id, idempotency_key="op-1")
    assert charged.status == "paid"
    assert charged.charge_id is not None


def test_retrying_with_the_same_key_does_not_double_charge():
    svc = OrderService()
    order = svc.create_order(amount_cents=2000)
    first = svc.charge_order(order.order_id, idempotency_key="op-2")
    second = svc.charge_order(order.order_id, idempotency_key="op-2")
    assert first.charge_id == second.charge_id


def test_full_refund():
    svc = OrderService()
    order = svc.create_order(amount_cents=2000)
    svc.charge_order(order.order_id, idempotency_key="op-3")
    refunded = svc.refund_order(order.order_id)
    assert refunded.status == "refunded"


def test_partial_refund_not_supported():
    svc = OrderService()
    order = svc.create_order(amount_cents=2000)
    svc.charge_order(order.order_id, idempotency_key="op-4")
    try:
        svc.refund_order(order.order_id, amount_cents=500)
    except NotImplementedError:
        pass
    else:
        raise AssertionError("expected NotImplementedError for a partial refund")
