#requires -Version 7.0
$ErrorActionPreference = "Stop"

Write-Host "Generating synthetic datasets..."

python - << 'PY'
import pandas as pd
import numpy as np
from pathlib import Path

root = Path(__file__).resolve().parents[2]
raw = root / 'data' / 'raw'
raw.mkdir(parents=True, exist_ok=True)

np.random.seed(42)
# Products
products = pd.DataFrame({
    'sku': [f'SKU-{i:05d}' for i in range(1, 201)],
    'category': np.random.choice(['Beverages','Snacks','PersonalCare','Household'], 200),
    'brand': np.random.choice(['BrandA','BrandB','BrandC'], 200)
})
products.to_csv(raw / 'products.csv', index=False)

# Locations
locations = pd.DataFrame({
    'location_id': [f'LOC-{i:03d}' for i in range(1, 31)],
    'type': np.random.choice(['Plant','DC','Store'], 30),
    'region': np.random.choice(['NORTH','SOUTH','EAST','WEST'], 30)
})
locations.to_csv(raw / 'locations.csv', index=False)

# Calendar
dates = pd.date_range('2024-01-01','2024-03-31')
calendar = pd.DataFrame({'date': dates, 'is_holiday': np.random.choice([0,1], len(dates), p=[0.95,0.05])})
calendar.to_csv(raw / 'calendar.csv', index=False)

# Orders
orders = []
for d in dates:
    for _ in range(np.random.poisson(80)):
        orders.append({
            'order_id': f'ORD-{np.random.randint(10**6)}',
            'date': d.date().isoformat(),
            'sku': np.random.choice(products['sku']),
            'qty': int(np.random.gamma(2, 5)),
            'location_id': np.random.choice(locations['location_id']),
            'channel': np.random.choice(['Retail','Ecom','B2B'])
        })
orders = pd.DataFrame(orders)
orders.to_csv(raw / 'orders.csv', index=False)

# Inventory
inv = []
for loc in locations['location_id']:
    for sku in products['sku'][:100]:
        inv.append({
            'location_id': loc,
            'sku': sku,
            'on_hand': int(np.random.gamma(3, 20))
        })
inv = pd.DataFrame(inv)
inv.to_csv(raw / 'inventory.csv', index=False)

# Transport events
trans = []
for i in range(1000):
    trans.append({
        'event_id': f'TEV-{i:06d}',
        'order_id': np.random.choice(orders['order_id']),
        'status': np.random.choice(['CREATED','DISPATCHED','IN_TRANSIT','DELIVERED']),
        'lat': float(np.random.uniform(-33.6,-33.2)),
        'lon': float(np.random.uniform(-70.8,-70.5))
    })
trans = pd.DataFrame(trans)
trans.to_csv(raw / 'transport_events.csv', index=False)

print('Done: products, locations, calendar, orders, inventory, transport_events')
PY

Write-Host "Synthetic datasets generated under data/raw"