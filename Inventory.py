import threading


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

    # --------------------------------
    # Add Product
    # --------------------------------
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

    # --------------------------------
    # Remove Product
    # --------------------------------
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

    # --------------------------------
    # Check Stock
    # --------------------------------
    def check_stock(self, warehouse, product):

        if warehouse not in self.warehouses:
            return None

        if product not in self.warehouses[warehouse]:
            return None

        return self.warehouses[warehouse][product]

    # --------------------------------
    # Transfer Stock
    # --------------------------------
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

    # --------------------------------
    # Supplier Management
    # --------------------------------
    def add_supplier(self, supplier_id, supplier_name):

        if supplier_id in self.suppliers:
            return False

        self.suppliers[supplier_id] = supplier_name

        return True

    # --------------------------------
    # Low Stock Detection
    # --------------------------------
    def low_stock(self, warehouse, product):

        stock = self.check_stock(
            warehouse,
            product
        )

        if stock is None:
            return False

        return stock <= self.reorder_threshold

    # --------------------------------
    # Reorder
    # --------------------------------
    def reorder(self, warehouse, product, quantity):

        if warehouse not in self.warehouses:
            return False

        if quantity <= 0:
            return False

        if product not in self.warehouses[warehouse]:
            self.warehouses[warehouse][product] = 0

        self.warehouses[warehouse][product] += quantity

        return True

    # --------------------------------
    # Warehouse Selection
    # --------------------------------
    def select_warehouse(self, product, quantity):

        for warehouse in ["A", "B", "C"]:

            if product in self.warehouses[warehouse]:

                if self.warehouses[warehouse][product] >= quantity:
                    return warehouse

        return None

    # --------------------------------
    # Fulfill Order
    # --------------------------------
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


# --------------------------------
# Main Program
# --------------------------------
if __name__ == "__main__":

    inventory = InventoryManagement()

    print("INVENTORY MANAGEMENT SYSTEM")
    print("============================")

    # Add products
    print(
        "Add Laptop to Warehouse A:",
        inventory.add_product("A", "Laptop", 50)
    )

    print(
        "Add Laptop to Warehouse B:",
        inventory.add_product("B", "Laptop", 30)
    )

    print(
        "Add Mobile to Warehouse C:",
        inventory.add_product("C", "Mobile", 20)
    )

    # Check stock
    print()
    print("Stock in Warehouse A:")
    print(
        inventory.check_stock("A", "Laptop")
    )

    # Remove product
    print()
    print(
        "Remove Laptop:",
        inventory.remove_product(
            "A",
            "Laptop",
            10
        )
    )

    # Transfer stock
    print()
    print(
        "Transfer Laptop A -> B:",
        inventory.transfer_stock(
            "A",
            "B",
            "Laptop",
            10
        )
    )

    # Supplier
    print()
    print(
        "Add Supplier:",
        inventory.add_supplier(
            "S001",
            "ABC Suppliers"
        )
    )

    # Low stock
    print()
    print(
        "Low Stock:",
        inventory.low_stock(
            "A",
            "Laptop"
        )
    )

    # Warehouse selection
    print()
    print(
        "Selected Warehouse:",
        inventory.select_warehouse(
            "Laptop",
            20
        )
    )

    # Fulfill order
    print()
    print(
        "Order Fulfilled:",
        inventory.fulfill_order(
            "Laptop",
            20
        )
    )
