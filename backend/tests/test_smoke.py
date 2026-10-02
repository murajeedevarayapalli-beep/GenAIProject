from app.config import get_settings


def test_settings_load():
    settings = get_settings()
    assert settings.app_name


def test_order_lookup():
    from app.tools.order_tools import get_order

    order = get_order("ORD-1001")
    assert order["order_id"] == "ORD-1001"
