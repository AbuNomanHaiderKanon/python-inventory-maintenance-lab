import sqlite3

import unittest

from inventory.db import connect
from inventory.service import InventoryError, Product, add_product, create_order, low_stock, restock, summary


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.conn = connect(":memory:")

    def tearDown(self):
        self.conn.close()

    def test_product_lifecycle(self):
        add_product(self.conn, Product("p-1", "Notebook", 3, 2, 500))
        self.assertEqual(restock(self.conn, "p-1", 4), 7)
        self.assertEqual(create_order(self.conn, "p-1", 2), 1000)
        self.assertEqual(summary(self.conn), {"products": 1, "units": 5, "orders": 1, "revenue_cents": 1000})

    def test_order_rejects_insufficient_stock(self):
        add_product(self.conn, Product("P-1", "Notebook", 1, 2, 500))
        with self.assertRaisesRegex(InventoryError, "Insufficient stock"):
            create_order(self.conn, "P-1", 2)

    def test_low_stock_report(self):
        add_product(self.conn, Product("P-1", "Notebook", 1, 2, 500))
        self.assertEqual([p.sku for p in low_stock(self.conn)], ["P-1"])
