class SingleResponsibilityBadExample:

    # we are a order management system which
    # checks inventory database if we have the required item according to the quantity
    # Item can be of two types ultra expensive and low expensive
    # If the item is available we need to reserve that item by reduce the inventory size
    # Item should be first packed for delivery (Gift Pack or Normal Pack depending on the order)
    # Once ready we need to finalize the vendor for shipping the product
        # Ultra expensive products must be shipped with EKART Logistics
        # Low expensive products must be shipped with Delhivery
    # EKART has their own of way of placing order for delivery
    # Delhivery has their own way of placing order for delivery

    def __init__(self,item_name,order_category,packaging_type):
        self.item_name =  item_name
        self.order_category = order_category
        self.packaging_type = packaging_type

    def connect_to_inventory_db_and_check_for_item(self):
        print( "DB is connected and item is found")
        return True

    # THIS IS A BAD EXAMPLE FOR SINGLE RESPONSIBILITY
    # place_order_with_delivery_partner should only be responsible for placing order
    # But we are doing entire functioning in it.

    def place_order_with_delivery_partner(self):
        # Check existance of item in inventory db
        if self.connect_to_inventory_db_and_check_for_item():
            if self.packaging_type == "GIFT":
                print("using gift wrap")
                print("adding the greeting card")
            elif self.packaging_type == "NORMAL":
                print("using normal wrap")
            # Check if category is Low expensive or ultra expensive
            if self.order_category == "LOW EXPENSIVE":
                # Assign the order to delhivery partner
                add_address = "some address"
                pay_through_token_system ="payment done"
            elif self.order_category == "ULTRA EXPENSIVE":
                # Assign the order to ekart partner
                add_address = "some address"
                pay_through_upi_system = "payment done"
                print("Order is assigned to EKART")

"""
SAME EXAMPLE ABOVE CHANGED USING S principle of solid
EACH CLASS MUST HAVE ONE SINGLE RESPONSIBILITY
EACH METHOD MUST HAVE ONE SINGLE RESPONSIBILITY
"""

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

class ShippingService:
    def ship_item(self, category):
        if category == "ULTRA EXPENSIVE":
            print("Shipping via EKART")
        else:
            print("Shipping via Delhivery")


# =========================
# ORDER RESPONSIBILITY
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



if __name__ == "__main__":
    main()












