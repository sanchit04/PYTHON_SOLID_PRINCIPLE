from abc import ABC, abstractmethod


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
# SHIPPING ABSTRACTION
# =========================
class ShippingService(ABC):

    @abstractmethod
    def ship_item(self):
        pass


# =========================
# LSP VIOLATING IMPLEMENTATION
# =========================
"""
IN this case EKART is only supporting ULTRA expensive shipments
If now a low expensive shipment is asked to be delivered it will raise exception
Whereas Shipping service base class (parent class) promises us the shipment will happen
But subclass EkartShippingService child is adding its own rule to decide
if shipment will happen or not this is a clear violation of Liskov substitution priciple
child should not change the behaviour of what parent has defined!
"""

class EkartShippingService(ShippingService):

    def __init__(self, category):
        self.category = category

    def ship_item(self):
        if self.category != "ULTRA_EXPENSIVE":
            raise Exception("EKART only supports ULTRA_EXPENSIVE items")
        print("Shipping via EKART")


class DelhiveryShippingService(ShippingService):
    def ship_item(self):
        print("Shipping via Delhivery")


# =========================
# ORDER SERVICE (Orchestrator)
# =========================
class OrderService:

    def __init__(self, category):
        self.inventory_service = InventoryService()
        self.packaging_service = PackagingService()

        if category == "ULTRA_EXPENSIVE":
            self.shipping_service = EkartShippingService(category)
        else:
            self.shipping_service = DelhiveryShippingService()

    def process_order(self, item_name, packaging_type):
        if self.inventory_service.check_item(item_name):
            self.inventory_service.reserve_item(item_name)
            self.packaging_service.package_item(packaging_type)
            self.shipping_service.ship_item()
            print("Order processed successfully")


# =========================
# GENERIC FUNCTION (To show LSP break)
# =========================
def test_shipping(shipping: ShippingService):
    print("\nTesting generic shipping function...")
    shipping.ship_item()


# =========================
# MAIN
# =========================
def main():

    print("---- Normal Order Flow ----")
    order_service = OrderService(category="LOW_EXPENSIVE")
    order_service.process_order(
        item_name="iPhone 16",
        packaging_type="NORMAL"
    )

    print("\n---- LSP Violation Demo ----")
    shipping = EkartShippingService("LOW_EXPENSIVE")
    test_shipping(shipping)   # This will raise Exception


if __name__ == "__main__":
    main()
