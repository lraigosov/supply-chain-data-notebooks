import pandas as pd
from pathlib import Path
from src.utils.paths import DATA_RAW


def test_orders_schema():
    df = pd.read_csv(DATA_RAW / 'orders.csv')
    required_cols = {'order_id', 'date', 'sku', 'qty', 'location_id', 'channel'}
    assert required_cols.issubset(df.columns), f"Missing columns in orders.csv"
    assert df['qty'].dtype in ['int64', 'float64'], "qty must be numeric"
    assert not df['order_id'].isnull().any(), "order_id has nulls"


def test_inventory_schema():
    df = pd.read_csv(DATA_RAW / 'inventory.csv')
    required_cols = {'location_id', 'sku', 'on_hand'}
    assert required_cols.issubset(df.columns), f"Missing columns in inventory.csv"
    assert df['on_hand'].dtype in ['int64', 'float64'], "on_hand must be numeric"


def test_products_schema():
    df = pd.read_csv(DATA_RAW / 'products.csv')
    required_cols = {'sku', 'category', 'brand'}
    assert required_cols.issubset(df.columns), f"Missing columns in products.csv"
    assert not df['sku'].duplicated().any(), "Duplicate SKUs in products"
