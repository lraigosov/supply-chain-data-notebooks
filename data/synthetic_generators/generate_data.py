"""
Generador de datos sintéticos realistas para supply chain.
Ejecutar: python data/synthetic_generators/generate_data.py
"""
import pandas as pd
import numpy as np
from pathlib import Path

root = Path(__file__).resolve().parents[2]
raw = root / 'data' / 'raw'
raw.mkdir(parents=True, exist_ok=True)

np.random.seed(42)

print("Generando datasets sintéticos...")

# Products: portafolio realista
categories = ['Beverages', 'Snacks', 'PersonalCare', 'Household', 'Electronics']
brands = ['BrandA', 'BrandB', 'BrandC', 'BrandD', 'BrandE']
products = pd.DataFrame({
    'sku': [f'SKU-{i:05d}' for i in range(1, 201)],
    'category': np.random.choice(categories, 200),
    'brand': np.random.choice(brands, 200),
    'unit_cost': np.round(np.random.uniform(5, 150, 200), 2)
})
products.to_csv(raw / 'products.csv', index=False)
print(f"✓ products.csv: {len(products)} SKUs")

# Locations: red logística
location_types = ['Plant', 'DC', 'Hub', 'Store']
regions = ['NORTH', 'SOUTH', 'EAST', 'WEST', 'CENTER']
locations = pd.DataFrame({
    'location_id': [f'LOC-{i:03d}' for i in range(1, 31)],
    'type': np.random.choice(location_types, 30, p=[0.1, 0.2, 0.2, 0.5]),
    'region': np.random.choice(regions, 30),
    'capacity': np.random.randint(1000, 50000, 30)
})
locations.to_csv(raw / 'locations.csv', index=False)
print(f"✓ locations.csv: {len(locations)} ubicaciones")

# Calendar: 90 días con festivos y promociones
dates = pd.date_range('2024-01-01', '2024-03-31')
calendar = pd.DataFrame({
    'date': dates,
    'is_holiday': np.random.choice([0, 1], len(dates), p=[0.93, 0.07]),
    'is_promo': np.random.choice([0, 1], len(dates), p=[0.85, 0.15]),
    'day_of_week': dates.dayofweek
})
calendar.to_csv(raw / 'calendar.csv', index=False)
print(f"✓ calendar.csv: {len(calendar)} días")

# Orders: órdenes diarias con estacionalidad
orders = []
order_id = 100000
for idx, d in enumerate(dates):
    # Estacionalidad: más órdenes en fines de semana y promociones
    base_volume = 80
    if d.dayofweek >= 5:  # fin de semana
        base_volume = 120
    if calendar.iloc[idx]['is_promo']:
        base_volume = int(base_volume * 1.3)
    
    n_orders = np.random.poisson(base_volume)
    
    for _ in range(n_orders):
        orders.append({
            'order_id': f'ORD-{order_id}',
            'date': d.date().isoformat(),
            'sku': np.random.choice(products['sku']),
            'qty': int(np.random.gamma(2, 5)),
            'location_id': np.random.choice(locations['location_id']),
            'channel': np.random.choice(['Retail', 'Ecom', 'B2B'], p=[0.5, 0.3, 0.2])
        })
        order_id += 1

orders = pd.DataFrame(orders)
orders.to_csv(raw / 'orders.csv', index=False)
print(f"✓ orders.csv: {len(orders)} órdenes")

# Inventory: niveles de stock por SKU/Location
inv = []
for loc in locations['location_id']:
    # Solo ~50% de SKUs por location
    skus_in_loc = np.random.choice(products['sku'], size=100, replace=False)
    for sku in skus_in_loc:
        inv.append({
            'location_id': loc,
            'sku': sku,
            'on_hand': int(np.random.gamma(3, 20))
        })

inv = pd.DataFrame(inv)
inv.to_csv(raw / 'inventory.csv', index=False)
print(f"✓ inventory.csv: {len(inv)} registros de inventario")

# Transport events: tracking de entregas
trans = []
statuses = ['CREATED', 'DISPATCHED', 'IN_TRANSIT', 'DELIVERED', 'DELAYED']
sampled_orders = orders.sample(n=min(1000, len(orders)), random_state=42)

for _, order_row in sampled_orders.iterrows():
    # Simular eventos progresivos
    n_events = np.random.randint(2, 5)
    for i in range(n_events):
        trans.append({
            'event_id': f'TEV-{len(trans):06d}',
            'order_id': order_row['order_id'],
            'status': statuses[min(i, len(statuses)-1)],
            'lat': float(np.random.uniform(-33.6, -33.2)),
            'lon': float(np.random.uniform(-70.8, -70.5)),
            'timestamp': pd.Timestamp(order_row['date']) + pd.Timedelta(hours=i*6)
        })

trans = pd.DataFrame(trans)
trans.to_csv(raw / 'transport_events.csv', index=False)
print(f"✓ transport_events.csv: {len(trans)} eventos de transporte")

print("\n✅ Datos sintéticos generados exitosamente en data/raw/")
