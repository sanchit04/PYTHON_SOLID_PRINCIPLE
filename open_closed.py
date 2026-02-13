"""
FOLLOWING IS THE SAME EXAMPLE lets see if we have any leverage to use open closed
"""

class InventoryService:
    def check_item(self, item_name):
        print(f"Checking DB for {item_name}")
        return True


class PackagingService:
    def package(self, packaging_type):
        if packaging_type == "GIFT":
            print("using gift wrap")
        else:
            print("using normal wrap")


class ShippingService:
    def ship(self, category):
        if category == "LOW EXPENSIVE":
            print("Assigned to Delhivery")
        else:
            print("Assigned to EKART")

# USED THIS AS A COMPOSITION CLASS TO GLUE ALL TOGETHER
class OrderService:
    def __init__(self, inventory, packaging, shipping):
        self.inventory = inventory
        self.packaging = packaging
        self.shipping = shipping

    def process_order(self, item, category, packaging_type):
        if self.inventory.check_item(item):
            self.packaging.package(packaging_type)
            self.shipping.ship(category)


def main():
    # Create individual services
    inventory_service = InventoryService()
    packaging_service = PackagingService()
    shipping_service = ShippingService()

    # Inject dependencies into OrderService
    order_service = OrderService(
        inventory=inventory_service,
        packaging=packaging_service,
        shipping=shipping_service
    )

    # Process an order
    order_service.process_order(
        item="iPhone 16",
        category="ULTRA EXPENSIVE",
        packaging_type="GIFT"
    )


if __name__ == "__main__":
    main()