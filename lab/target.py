"""Small deterministic workload shared by the four lab experiments."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from inventory.db import connect
from inventory.service import Product, add_product, create_order, low_stock, restock, summary


def build_demo_database():
    conn = connect(":memory:")
    for product in (
        Product("P-100", "Wireless Mouse", 25, 10, 1550),
        Product("P-200", "Mechanical Keyboard", 8, 5, 7200),
        Product("P-300", "USB-C Cable", 40, 15, 899),
    ):
        add_product(conn, product)
    return conn


def process_orders(conn) -> dict[str, int]:
    """Run a representative maintenance workload and return a summary."""
    restock(conn, "P-200", 4)
    create_order(conn, "P-100", 3)
    create_order(conn, "P-200", 2)
    create_order(conn, "P-300", 7)
    result = summary(conn)
    result["low_stock_items"] = len(low_stock(conn))
    return result


def run_workload() -> dict[str, int]:
    conn = build_demo_database()
    try:
        return process_orders(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    print(run_workload())
