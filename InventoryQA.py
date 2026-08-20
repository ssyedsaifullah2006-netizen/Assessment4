import unittest
import threading
from InventoryManagement import InventorySystem


class TestInventory(unittest.TestCase):

    def setUp(self):
        self.inventory = InventorySystem()

        self.inventory.add_product("A", "Laptop", 100)
        self.inventory.add_product("B", "Laptop", 50)
        self.inventory.add_product("C", "Laptop", 25)

        self.inventory.add_supplier("ABC Suppliers", "Laptop")
        self.inventory.set_reorder("Laptop", 30, 50)

    # 1. Stock availability
    def test_stock_availability(self):
        result, message = self.inventory.fulfill_order(
            "Laptop", 20
        )

        self.assertTrue(result)

    # 2. Insufficient inventory
    def test_insufficient_inventory(self):
        result, message = self.inventory.fulfill_order(
            "Laptop", 500
        )

        self.assertFalse(result)
        self.assertEqual(message, "Insufficient inventory")

    # 3. Warehouse transfer
    def test_warehouse_transfer(self):
        result, message = self.inventory.transfer_stock(
            "A", "B", "Laptop", 20
        )

        self.assertTrue(result)

        self.assertEqual(
            self.inventory.warehouses["A"]["Laptop"],
            80
        )

        self.assertEqual(
            self.inventory.warehouses["B"]["Laptop"],
            70
        )

    # 4. Concurrent orders
    def test_concurrent_orders(self):

        def order():
            self.inventory.fulfill_order(
                "Laptop", 10
            )

        threads = []

        for i in range(5):
            t = threading.Thread(target=order)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        total = self.inventory.total_stock("Laptop")

        self.assertEqual(total, 125)

    # 5. Reorder threshold
    def test_reorder_threshold(self):

        # Remove stock until total becomes <= 30
        self.inventory.remove_product("A", "Laptop", 100)
        self.inventory.remove_product("B", "Laptop", 50)

        result, message = self.inventory.reorder("Laptop")

        self.assertTrue(result)

    # 6. Invalid product
    def test_invalid_product(self):

        result, message = self.inventory.remove_product(
            "A", "Tablet", 10
        )

        self.assertFalse(result)
        self.assertEqual(message, "Invalid product")

    # 7. Negative inventory
    def test_negative_inventory(self):

        result, message = self.inventory.add_product(
            "A", "Laptop", -10
        )

        self.assertFalse(result)
        self.assertEqual(
            message,
            "Negative inventory not allowed"
        )

    # 8. Multiple warehouses
    def test_multiple_warehouses(self):

        self.assertIn(
            "Laptop",
            self.inventory.warehouses["A"]
        )

        self.assertIn(
            "Laptop",
            self.inventory.warehouses["B"]
        )

        self.assertIn(
            "Laptop",
            self.inventory.warehouses["C"]
        )


if __name__ == "__main__":
    unittest.main()