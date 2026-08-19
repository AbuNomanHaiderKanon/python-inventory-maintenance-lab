from __future__ import annotations

import sqlite3
from dataclasses import dataclass


class InventoryError(ValueError):
    """Raised when an inventory operation cannot be completed."""


@dataclass(frozen=True)
class Product:
    sku: str
    name: str
    quantity: int
    reorder_level: int
    price_cents: int


def add_product(conn: sqlite3.Connection, product: Product) -> None:
    if not product.sku.strip() or not product.name.strip():
        raise InventoryError("SKU and name are required")
    if product.quantity < 0 or product.reorder_level < 0 or product.price_cents < 0:
        raise InventoryError("Quantity, reorder level, and price must be non-negative")
    try:
        conn.execute(
            "INSERT INTO products (sku, name, quantity, reorder_level, price_cents) VALUES (?, ?, ?, ?, ?)",
            (product.sku.strip().upper(), product.name.strip(), product.quantity, product.reorder_level, product.price_cents),
        )
        conn.commit()
    except sqlite3.IntegrityError as exc:
        raise InventoryError(f"Product {product.sku} already exists") from exc


def restock(conn: sqlite3.Connection, sku: str, quantity: int) -> int:
    if quantity <= 0:
        raise InventoryError("Restock quantity must be positive")
    result = conn.execute("UPDATE products SET quantity = quantity + ? WHERE sku = ?", (quantity, sku.upper()))
    if result.rowcount == 0:
        raise InventoryError(f"Unknown product: {sku}")
    conn.commit()
    return conn.execute("SELECT quantity FROM products WHERE sku = ?", (sku.upper(),)).fetchone()[0]


def create_order(conn: sqlite3.Connection, sku: str, quantity: int) -> int:
    if quantity <= 0:
        raise InventoryError("Order quantity must be positive")
    product = conn.execute("SELECT * FROM products WHERE sku = ?", (sku.upper(),)).fetchone()
    if product is None:
        raise InventoryError(f"Unknown product: {sku}")
    if product["quantity"] < quantity:
        raise InventoryError(f"Insufficient stock for {sku}: {product['quantity']} available")
    total = product["price_cents"] * quantity
    with conn:
        conn.execute("UPDATE products SET quantity = quantity - ? WHERE sku = ?", (quantity, sku.upper()))
        conn.execute("INSERT INTO orders (sku, quantity, total_cents) VALUES (?, ?, ?)", (sku.upper(), quantity, total))
    return total


def list_products(conn: sqlite3.Connection) -> list[Product]:
    rows = conn.execute("SELECT * FROM products ORDER BY sku").fetchall()
    return [Product(row["sku"], row["name"], row["quantity"], row["reorder_level"], row["price_cents"]) for row in rows]


def low_stock(conn: sqlite3.Connection) -> list[Product]:
    return [p for p in list_products(conn) if p.quantity <= p.reorder_level]


def summary(conn: sqlite3.Connection) -> dict[str, int]:
    row = conn.execute("SELECT COUNT(*) AS products, COALESCE(SUM(quantity), 0) AS units FROM products").fetchone()
    orders = conn.execute("SELECT COUNT(*) AS count, COALESCE(SUM(total_cents), 0) AS revenue FROM orders").fetchone()
    return {"products": row["products"], "units": row["units"], "orders": orders["count"], "revenue_cents": orders["revenue"]}
