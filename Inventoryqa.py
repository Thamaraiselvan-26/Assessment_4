import threading
import sys


# ==========================================
# Inventory Management Class
# ==========================================

class InventoryManagement:

    def __init__(self):

        self.warehouses = {
            "A": {},
            "B": {},
            "C": {}
        }

        self.suppliers = {}

        self.reorder_threshold = 10

        self.lock = threading.Lock()

    # Add Product
    def add_product(self, warehouse, product, quantity):

        if warehouse not in self.warehouses:
            return False

        if quantity <= 0:
            return False

        if product in self.warehouses[warehouse]:
            self.warehouses[warehouse][product] += quantity
        else:
            self.warehouses[warehouse][product] = quantity

        return True

    # Remove Product
    def remove_product(self, warehouse, product, quantity):

        if warehouse not in self.warehouses:
            return False

        if product not in self.warehouses[warehouse]:
            return False

        if quantity <= 0:
            return False

        if self.warehouses[warehouse][product] < quantity:
            return False

        with self.lock:

            self.warehouses[warehouse][product] -= quantity

        return True

    # Check Stock
    def check_stock(self, warehouse, product):

        if warehouse not in self.warehouses:
            return None

        if product not in self.warehouses[warehouse]:
            return None

        return self.warehouses[warehouse][product]

    # Transfer Stock
    def transfer_stock(
        self,
        source,
        destination,
        product,
        quantity
    ):

        if source not in self.warehouses:
            return False

        if destination not in self.warehouses:
            return False

        if product not in self.warehouses[source]:
            return False

        if quantity <= 0:
            return False

        if self.warehouses[source][product] < quantity:
            return False

        with self.lock:

            self.warehouses[source][product] -= quantity

            if product in self.warehouses[destination]:
                self.warehouses[destination][product] += quantity
            else:
                self.warehouses[destination][product] = quantity

        return True

    # Supplier Management
    def add_supplier(self, supplier_id, supplier_name):

        if supplier_id in self.suppliers:
            return False

        self.suppliers[supplier_id] = supplier_name

        return True

    # Low Stock
    def low_stock(self, warehouse, product):

        stock = self.check_stock(
            warehouse,
            product
        )

        if stock is None:
            return False

        return stock <= self.reorder_threshold

    # Reorder
    def reorder(self, warehouse, product, quantity):

        if warehouse not in self.warehouses:
            return False

        if quantity <= 0:
            return False

        if product not in self.warehouses[warehouse]:
            self.warehouses[warehouse][product] = 0

        self.warehouses[warehouse][product] += quantity

        return True

    # Automatic Warehouse Selection
    def select_warehouse(self, product, quantity):

        for warehouse in ["A", "B", "C"]:

            if product in self.warehouses[warehouse]:

                if self.warehouses[warehouse][product] >= quantity:
                    return warehouse

        return None

    # Fulfill Order
    def fulfill_order(self, product, quantity):

        warehouse = self.select_warehouse(
            product,
            quantity
        )

        if warehouse is None:
            return False

        with self.lock:

            self.warehouses[warehouse][product] -= quantity

        return True


# ==========================================
# Test Counter
# ==========================================

passed = 0
failed = 0


def check_test(name, result):

    global passed
    global failed

    if result:

        print("PASS - " + name)
        passed += 1

    else:

        print("FAIL - " + name)
        failed += 1


# ==========================================
# 1. Stock Availability
# ==========================================

def test_stock_availability():

    inventory = InventoryManagement()

    inventory.add_product(
        "A",
        "Laptop",
        50
    )

    stock = inventory.check_stock(
        "A",
        "Laptop"
    )

    check_test(
        "Stock Availability",
        stock == 50
    )


# ==========================================
# 2. Insufficient Inventory
# ==========================================

def test_insufficient_inventory():

    inventory = InventoryManagement()

    inventory.add_product(
        "A",
        "Laptop",
        10
    )

    result = inventory.remove_product(
        "A",
        "Laptop",
        20
    )

    check_test(
        "Insufficient Inventory",
        result is False
    )


# ==========================================
# 3. Warehouse Transfer
# ==========================================

def test_warehouse_transfer():

    inventory = InventoryManagement()

    inventory.add_product(
        "A",
        "Laptop",
        50
    )

    result = inventory.transfer_stock(
        "A",
        "B",
        "Laptop",
        20
    )

    stock_a = inventory.check_stock(
        "A",
        "Laptop"
    )

    stock_b = inventory.check_stock(
        "B",
        "Laptop"
    )

    check_test(
        "Warehouse Transfer",
        result is True
        and stock_a == 30
        and stock_b == 20
    )


# ==========================================
# 4. Concurrent Orders
# ==========================================

def order_thread(inventory):

    inventory.fulfill_order(
        "Laptop",
        10
    )


def test_concurrent_orders():

    inventory = InventoryManagement()

    inventory.add_product(
        "A",
        "Laptop",
        100
    )

    threads = []

    for i in range(5):

        thread = threading.Thread(
            target=order_thread,
            args=(inventory,)
        )

        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    stock = inventory.check_stock(
        "A",
        "Laptop"
    )

    check_test(
        "Concurrent Orders",
        stock == 50
    )


# ==========================================
# 5. Reorder Threshold
# ==========================================

def test_reorder_threshold():

    inventory = InventoryManagement()

    inventory.add_product(
        "A",
        "Laptop",
        5
    )

    result = inventory.low_stock(
        "A",
        "Laptop"
    )

    check_test(
        "Reorder Threshold",
        result is True
    )


# ==========================================
# 6. Invalid Product
# ==========================================

def test_invalid_product():

    inventory = InventoryManagement()

    result = inventory.remove_product(
        "A",
        "Mobile",
        5
    )

    check_test(
        "Invalid Product",
        result is False
    )


# ==========================================
# 7. Negative Inventory
# ==========================================

def test_negative_inventory():

    inventory = InventoryManagement()

    result = inventory.add_product(
        "A",
        "Laptop",
        -10
    )

    check_test(
        "Negative Inventory",
        result is False
    )


# ==========================================
# 8. Multiple Warehouses
# ==========================================

def test_multiple_warehouses():

    inventory = InventoryManagement()

    inventory.add_product(
        "A",
        "Laptop",
        10
    )

    inventory.add_product(
        "B",
        "Laptop",
        20
    )

    inventory.add_product(
        "C",
        "Laptop",
        30
    )

    stock_a = inventory.check_stock(
        "A",
        "Laptop"
    )

    stock_b = inventory.check_stock(
        "B",
        "Laptop"
    )

    stock_c = inventory.check_stock(
        "C",
        "Laptop"
    )

    check_test(
        "Multiple Warehouses",
        stock_a == 10
        and stock_b == 20
        and stock_c == 30
    )


# ==========================================
# 9. Warehouse Selection
# ==========================================

def test_warehouse_selection():

    inventory = InventoryManagement()

    inventory.add_product(
        "A",
        "Laptop",
        5
    )

    inventory.add_product(
        "B",
        "Laptop",
        20
    )

    inventory.add_product(
        "C",
        "Laptop",
        30
    )

    warehouse = inventory.select_warehouse(
        "Laptop",
        15
    )

    check_test(
        "Warehouse Selection",
        warehouse == "B"
    )


# ==========================================
# 10. Supplier Management
# ==========================================

def test_supplier_management():

    inventory = InventoryManagement()

    result = inventory.add_supplier(
        "S001",
        "ABC Suppliers"
    )

    check_test(
        "Supplier Management",
        result is True
    )


# ==========================================
# Run All Tests
# ==========================================

if __name__ == "__main__":

    print()
    print("========================================")
    print("       INVENTORY MANAGEMENT QA")
    print("========================================")

    test_stock_availability()

    test_insufficient_inventory()

    test_warehouse_transfer()

    test_concurrent_orders()

    test_reorder_threshold()

    test_invalid_product()

    test_negative_inventory()

    test_multiple_warehouses()

    test_warehouse_selection()

    test_supplier_management()

    print()
    print("========================================")
    print("Tests Passed :", passed)
    print("Tests Failed :", failed)
    print("========================================")

    if failed == 0:

        print("ALL TESTS PASSED")

        sys.exit(0)

    else:

        print("TESTS FAILED")

        sys.exit(1)
