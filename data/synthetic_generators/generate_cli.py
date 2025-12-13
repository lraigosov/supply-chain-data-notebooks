"""
CLI cross-platform para generar datos sintéticos de supply chain.

Permite generar datos completos o muestras rápidas para testing.

Uso:
  python data/synthetic_generators/generate_cli.py              # Genera completo (90 días, 200 SKUs)
  python data/synthetic_generators/generate_cli.py --fast       # Genera rápido (7 días, 20 SKUs)
  python data/synthetic_generators/generate_cli.py --seed 123   # Reproducible con semilla
  python data/synthetic_generators/generate_cli.py --output /custom/path
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def generate_products(
    n_skus: int = 200,
    seed: int | None = None,
) -> pd.DataFrame:
    """Generate product master data."""
    if seed is not None:
        np.random.seed(seed)

    categories = ["Beverages", "Snacks", "PersonalCare", "Household", "Electronics"]
    brands = ["BrandA", "BrandB", "BrandC", "BrandD", "BrandE"]

    products = pd.DataFrame({
        "sku": [f"SKU-{i:05d}" for i in range(1, n_skus + 1)],
        "category": np.random.choice(categories, n_skus),
        "brand": np.random.choice(brands, n_skus),
        "unit_cost": np.round(np.random.uniform(5, 150, n_skus), 2),
    })
    return products


def generate_locations(n_locs: int = 30, seed: int | None = None) -> pd.DataFrame:
    """Generate location/warehouse network."""
    if seed is not None:
        np.random.seed(seed)

    location_types = ["Plant", "DC", "Hub", "Store"]
    regions = ["NORTH", "SOUTH", "EAST", "WEST", "CENTER"]

    locations = pd.DataFrame({
        "location_id": [f"LOC-{i:03d}" for i in range(1, n_locs + 1)],
        "type": np.random.choice(location_types, n_locs, p=[0.1, 0.2, 0.2, 0.5]),
        "region": np.random.choice(regions, n_locs),
        "capacity": np.random.randint(1000, 50000, n_locs),
    })
    return locations


def generate_calendar(
    start_date: str = "2024-01-01",
    end_date: str = "2024-03-31",
    seed: int | None = None,
) -> pd.DataFrame:
    """Generate calendar with holidays and promos."""
    if seed is not None:
        np.random.seed(seed)

    dates = pd.date_range(start_date, end_date)
    calendar = pd.DataFrame({
        "date": dates,
        "is_holiday": np.random.choice([0, 1], len(dates), p=[0.93, 0.07]),
        "is_promo": np.random.choice([0, 1], len(dates), p=[0.85, 0.15]),
        "day_of_week": dates.dayofweek,
    })
    return calendar


def generate_orders(
    products: pd.DataFrame,
    locations: pd.DataFrame,
    calendar: pd.DataFrame,
    seed: int | None = None,
) -> pd.DataFrame:
    """Generate orders with seasonality."""
    if seed is not None:
        np.random.seed(seed)

    orders = []
    order_id = 100000
    dates = pd.to_datetime(calendar["date"])

    for idx, d in enumerate(dates):
        base_volume = 80
        if d.dayofweek >= 5:  # weekend
            base_volume = 120
        if calendar.iloc[idx]["is_promo"]:
            base_volume = int(base_volume * 1.3)

        n_orders = np.random.poisson(base_volume)

        for _ in range(n_orders):
            orders.append({
                "order_id": f"ORD-{order_id}",
                "date": d.date().isoformat(),
                "sku": np.random.choice(products["sku"]),
                "qty": int(np.random.gamma(2, 5)),
                "location_id": np.random.choice(locations["location_id"]),
                "channel": np.random.choice(["Retail", "Ecom", "B2B"], p=[0.5, 0.3, 0.2]),
            })
            order_id += 1

    return pd.DataFrame(orders)


def generate_inventory(
    products: pd.DataFrame,
    locations: pd.DataFrame,
    seed: int | None = None,
) -> pd.DataFrame:
    """Generate inventory levels."""
    if seed is not None:
        np.random.seed(seed)

    inv = []
    for loc in locations["location_id"]:
        # ~50% of SKUs per location
        n_skus = max(1, len(products) // 2)
        skus_in_loc = np.random.choice(products["sku"], size=n_skus, replace=False)
        for sku in skus_in_loc:
            inv.append({
                "location_id": loc,
                "sku": sku,
                "on_hand": int(np.random.gamma(3, 20)),
            })

    return pd.DataFrame(inv)


def generate_transport_events(
    orders: pd.DataFrame,
    seed: int | None = None,
) -> pd.DataFrame:
    """Generate transport tracking events."""
    if seed is not None:
        np.random.seed(seed)

    trans = []
    statuses = ["CREATED", "DISPATCHED", "IN_TRANSIT", "DELIVERED", "DELAYED"]
    sampled_orders = orders.sample(n=min(1000, len(orders)), random_state=seed)

    for _, order_row in sampled_orders.iterrows():
        n_events = np.random.randint(2, 5)
        for i in range(n_events):
            trans.append({
                "event_id": f"TEV-{len(trans):06d}",
                "order_id": order_row["order_id"],
                "status": statuses[min(i, len(statuses) - 1)],
                "lat": float(np.random.uniform(-33.6, -33.2)),
                "lon": float(np.random.uniform(-70.8, -70.5)),
                "timestamp": pd.Timestamp(order_row["date"]) + pd.Timedelta(hours=i * 6),
            })

    return pd.DataFrame(trans)


def generate_all(
    output_dir: Path,
    mode: str = "full",
    seed: int | None = None,
) -> dict[str, str]:
    """Generate all datasets and save to output_dir."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Mode-specific parameters
    params = {
        "full": {
            "n_skus": 200,
            "n_locs": 30,
            "date_range": ("2024-01-01", "2024-03-31"),
        },
        "fast": {
            "n_skus": 20,
            "n_locs": 5,
            "date_range": ("2024-01-01", "2024-01-07"),
        },
    }

    if mode not in params:
        raise ValueError(f"Unknown mode: {mode}. Choose 'full' or 'fast'.")

    p = params[mode]

    print(f"[GEN] Mode: {mode} | SKUs: {p['n_skus']} | Locations: {p['n_locs']}")

    # Generate datasets
    products = generate_products(n_skus=p["n_skus"], seed=seed)
    locations = generate_locations(n_locs=p["n_locs"], seed=seed)
    calendar = generate_calendar(start_date=p["date_range"][0], end_date=p["date_range"][1], seed=seed)
    orders = generate_orders(products, locations, calendar, seed=seed)
    inventory = generate_inventory(products, locations, seed=seed)
    transport = generate_transport_events(orders, seed=seed)

    # Save
    files = {
        "products.csv": products,
        "locations.csv": locations,
        "calendar.csv": calendar,
        "orders.csv": orders,
        "inventory.csv": inventory,
        "transport_events.csv": transport,
    }

    results = {}
    for fname, df in files.items():
        fpath = output_dir / fname
        df.to_csv(fpath, index=False)
        results[fname] = str(fpath)
        print(f"  ✓ {fname}: {len(df)} rows")

    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate synthetic supply chain datasets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
        "  python data/synthetic_generators/generate_cli.py\n"
        "  python data/synthetic_generators/generate_cli.py --fast\n"
        "  python data/synthetic_generators/generate_cli.py --seed 123 --output /tmp/data\n",
    )
    parser.add_argument(
        "--mode",
        choices=["full", "fast"],
        default="full",
        help="'full' for 90 days, 200 SKUs; 'fast' for 7 days, 20 SKUs (default: full)",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        help="Shorthand for --mode fast",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility (default: 42)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output directory (default: data/raw/ in repo root)",
    )

    args = parser.parse_args()

    mode = "fast" if args.fast else args.mode

    # Determine output directory
    if args.output:
        output_dir = args.output
    else:
        repo_root = Path(__file__).resolve().parents[2]
        output_dir = repo_root / "data" / "raw"

    print(f"📊 Generating synthetic datasets...")
    print(f"   Output: {output_dir}")

    try:
        results = generate_all(output_dir, mode=mode, seed=args.seed)
        print(f"\n✅ Done! Generated {len(results)} datasets.")
    except Exception as exc:
        print(f"\n❌ Error: {exc}")
        raise


if __name__ == "__main__":
    main()
