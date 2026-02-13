# EXAMPLE WHERE OCP IS NOT YET APPLIED ONLY S IS APPLIED

# =========================
# INVENTORY RESPONSIBILITY
# =========================

class InventoryService:
    def check_item(self, item_name):
        print(f"Checking inventory for {item_name}")
        return True

    def reserve_item(self, item_name):
        print(f"Reserving {item_name} from inventory")


# =========================
# PACKAGING RESPONSIBILITY
# =========================

class PackagingService:
    def package_item(self, packaging_type):
        if packaging_type == "GIFT":
            print("Using gift wrap")
            print("Adding greeting card")
        else:
            print("Using normal wrap")


# =========================
# SHIPPING RESPONSIBILITY
# =========================

"""
In this case we are violating OCP open closed principal
Our code should be open for extension but it should be closed for modification
In this case tomorrow lets say we get a new category 
MEDIUM expensive in that case we will have to modify ship_item to include a new category
That violates OCP

OCP usually appears where:
There are conditionals (if, switch)
Behavior varies by type
Future expansion is expected

Class Shipping Service should be changed to ABC so that it gets closed 
for modification and we can extend it based on subclasses
"""

class ShippingService:
    def ship_item(self, category):
        if category == "ULTRA EXPENSIVE":
            print("Shipping via EKART")
        else:
            print("Shipping via Delhivery")


# =========================
# ORDER RESPONSIBILITY KIND OF ACT AS A ORCHESTRATOR SINCE WE ARE DEALING WITH MULTIPLE SERVICES
# Why we can't do this in main itself? Its not correct main should only act as an entry point
# we should not add business logic to it
# =========================

class OrderService:
    def __init__(self):
        self.inventory_service = InventoryService()
        self.packaging_service = PackagingService()
        self.shipping_service = ShippingService()

    def process_order(self, item_name, category, packaging_type):
        if self.inventory_service.check_item(item_name):
            self.inventory_service.reserve_item(item_name)
            self.packaging_service.package_item(packaging_type)
            self.shipping_service.ship_item(category)
            print("Order processed successfully")


# =========================
# MAIN METHOD
# =========================

def main():
    order_service = OrderService()
    order_service.process_order(
        item_name="iPhone 16",
        category="ULTRA EXPENSIVE",
        packaging_type="GIFT"
    )


if __name__ == "__main__":
    main()


