import threading


class InventorySystem:

    def __init__(self):
        self.warehouses = {
            "A": {},
            "B": {},
            "C": {}
        }

        self.suppliers = {}
        self.reorder_threshold = {}
        self.reorder_quantity = {}
        self.lock = threading.Lock()

    # Add a product to a warehouse
    def add_product(self, warehouse, product, quantity):
        if warehouse not in self.warehouses:
            return False, "Invalid warehouse"

        if quantity < 0:
            return False, "Negative inventory not allowed"

        with self.lock:
            self.warehouses[warehouse][product] = \
                self.warehouses[warehouse].get(product, 0) + quantity

        return True, "Product added"

    # Remove product from warehouse
    def remove_product(self, warehouse, product, quantity):
        if warehouse not in self.warehouses:
            return False, "Invalid warehouse"

        if quantity < 0:
            return False, "Negative quantity not allowed"

        if product not in self.warehouses[warehouse]:
            return False, "Invalid product"

        with self.lock:
            if self.warehouses[warehouse][product] < quantity:
                return False, "Insufficient inventory"

            self.warehouses[warehouse][product] -= quantity

        return True, "Product removed"

    # Transfer stock between warehouses
    def transfer_stock(self, source, destination, product, quantity):
        if source not in self.warehouses or destination not in self.warehouses:
            return False, "Invalid warehouse"

        if source == destination:
            return False, "Source and destination cannot be same"

        if quantity <= 0:
            return False, "Invalid quantity"

        if product not in self.warehouses[source]:
            return False, "Invalid product"

        with self.lock:
            if self.warehouses[source][product] < quantity:
                return False, "Insufficient inventory"

            self.warehouses[source][product] -= quantity

            self.warehouses[destination][product] = \
                self.warehouses[destination].get(product, 0) + quantity

        return True, "Stock transferred"

    # Supplier management
    def add_supplier(self, supplier, product):
        self.suppliers[product] = supplier
        return True, "Supplier added"

    # Set reorder information
    def set_reorder(self, product, threshold, quantity):
        if threshold < 0 or quantity <= 0:
            return False, "Invalid reorder values"

        self.reorder_threshold[product] = threshold
        self.reorder_quantity[product] = quantity

        return True, "Reorder rule added"

    # Find total stock of a product
    def total_stock(self, product):
        total = 0

        for warehouse in self.warehouses:
            total += self.warehouses[warehouse].get(product, 0)

        return total

    # Low-stock detection
    def is_low_stock(self, product):
        if product not in self.reorder_threshold:
            return False

        return self.total_stock(product) <= self.reorder_threshold[product]

    # Reorder product
    def reorder(self, product):
        if product not in self.reorder_threshold:
            return False, "Reorder rule not configured"

        if product not in self.suppliers:
            return False, "Supplier not available"

        if not self.is_low_stock(product):
            return False, "Stock level is sufficient"

        quantity = self.reorder_quantity[product]

        # Reorder into warehouse with lowest stock
        warehouse = self.select_warehouse(product)

        self.warehouses[warehouse][product] = \
            self.warehouses[warehouse].get(product, 0) + quantity

        return True, "Product reordered"

    # Automatically select warehouse with stock
    def select_warehouse(self, product):
        available = []

        for warehouse in self.warehouses:
            stock = self.warehouses[warehouse].get(product, 0)

            if stock > 0:
                available.append((warehouse, stock))

        if not available:
            return None

        # Select warehouse with highest available stock
        available.sort(key=lambda x: x[1], reverse=True)

        return available[0][0]

    # Fulfill an order automatically
    def fulfill_order(self, product, quantity):
        if quantity <= 0:
            return False, "Invalid quantity"

        warehouse = self.select_warehouse(product)

        if warehouse is None:
            return False, "Product unavailable"

        if self.warehouses[warehouse][product] < quantity:
            return False, "Insufficient inventory"

        with self.lock:
            self.warehouses[warehouse][product] -= quantity

        return True, "Order fulfilled from Warehouse " + warehouse

    # Display inventory
    def show_inventory(self):
        for warehouse in self.warehouses:
            print("Warehouse", warehouse,
                  self.warehouses[warehouse])


if __name__ == "__main__":

    inventory = InventorySystem()

    inventory.add_product("A", "Laptop", 50)
    inventory.add_product("B", "Laptop", 30)
    inventory.add_product("C", "Laptop", 20)

    inventory.add_product("A", "Phone", 10)
    inventory.add_product("B", "Phone", 40)

    inventory.add_supplier("ABC Suppliers", "Laptop")
    inventory.set_reorder("Laptop", 20, 50)

    inventory.show_inventory()

    print(inventory.fulfill_order("Laptop", 10))
    print(inventory.transfer_stock("A", "C", "Laptop", 5))

    inventory.show_inventory()