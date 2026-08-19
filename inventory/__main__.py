from __future__ import annotations

import argparse

from .db import connect
from .service import Product, add_product, create_order, list_products, low_stock, restock, summary


def money(cents: int) -> str:
    return f"${cents / 100:.2f}"


def seed(conn) -> None:
    if list_products(conn):
        print("Database already contains products")
        return
    for product in [
        Product("P-100", "Wireless Mouse", 25, 10, 1550),
        Product("P-200", "Mechanical Keyboard", 8, 5, 7200),
        Product("P-300", "USB-C Cable", 40, 15, 899),
    ]:
        add_product(conn, product)
    print("Seed data inserted")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Inventory and order management")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("seed")
    sub.add_parser("list-products")
    sub.add_parser("report")
    add = sub.add_parser("add-product")
    add.add_argument("sku"); add.add_argument("name"); add.add_argument("quantity", type=int); add.add_argument("price", type=float); add.add_argument("--reorder-level", type=int, default=5)
    restock_cmd = sub.add_parser("restock")
    restock_cmd.add_argument("sku"); restock_cmd.add_argument("quantity", type=int)
    order = sub.add_parser("order")
    order.add_argument("sku"); order.add_argument("quantity", type=int)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    conn = connect()
    try:
        if args.command == "seed":
            seed(conn)
        elif args.command == "add-product":
            add_product(conn, Product(args.sku, args.name, args.quantity, args.reorder_level, round(args.price * 100)))
            print(f"Added {args.sku.upper()}")
        elif args.command == "restock":
            print(f"New stock level: {restock(conn, args.sku, args.quantity)}")
        elif args.command == "order":
            print(f"Order created: {money(create_order(conn, args.sku, args.quantity))}")
        elif args.command == "list-products":
            for product in list_products(conn):
                print(f"{product.sku:8} {product.name:24} stock={product.quantity:3} price={money(product.price_cents)}")
        elif args.command == "report":
            data = summary(conn)
            print(f"Products: {data['products']} | Units: {data['units']} | Orders: {data['orders']} | Revenue: {money(data['revenue_cents'])}")
            for product in low_stock(conn):
                print(f"LOW STOCK: {product.sku} ({product.quantity} remaining)")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
