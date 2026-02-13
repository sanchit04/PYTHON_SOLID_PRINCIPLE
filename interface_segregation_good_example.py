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

"""
DELIHIVERY HAS STARTED SUPPORTING TRACK and ETA service
THIS SERVICE IS NOT AVAILABLE IN BLUEDAART
Since not SHIPPING SERVICE IS added track and etc as abstract all subclasses have to implement it
IN this case EKARTSHIPPINGSERVICE will have to implement it which has no feature of track and eta
THIS IS DIRECT VIOLATION OF INTERFACE SEGREGATION PRINCIPLE
ISP violation often leads to LSP violation.

PROBLEM:

class ShippingService(ABC):

    @abstractmethod
    def ship_item(self):
        pass

    @abstractmethod
    def track_service(self):
        pass

    @abstractmethod
    def eta_service(self):
        pass


FIX: 
Should segregate track and eta service seperately
"""

class Trackable(ABC):
    @abstractmethod
    def track_service(self):
        pass

class ETAChecker(ABC):
    @abstractmethod
    def eta_service(self):
        pass

class ShippingService(ABC):

    @abstractmethod
    def ship_item(self):
        pass


class EkartShippingService(ShippingService):

    def ship_item(self):
        print("Shipping via Ekart")
    # # WE HAD TO IMPLEMENT BOTH TRACK AND ETA HERE SINCE BASE CLASS DEMANDS IT
    # # ITS UNNECESSARY! STILL HAVE TO IMPLEMENT IT
    # def track_service(self):
    #     print("I dont know what to do here")
    #
    # def eta_service(self):
    #     print("I dont know what to do here")
    # NO EKART DOES NOT HAVE TO IMPLEMENT TRACK AND ETA SERVICE


class DelhiveryShippingService(ShippingService,ETAChecker,Trackable):
    def ship_item(self):
        print("Shipping via Delhivery")

    # SINCE DELHIVERY HAS THIS FEATURE ONLY DELHIVERY IMPLEMENTS
    def track_service(self):
        print("TRACKING IS ENABLED")

    def eta_service(self):
        print("ETA TO DELIVER IS 2 HOURS!")


# =========================
# ORDER SERVICE (Orchestrator)
# =========================
class OrderService:

    def __init__(self, category):
        self.inventory_service = InventoryService()
        self.packaging_service = PackagingService()

        if category == "ULTRA_EXPENSIVE":
            self.shipping_service = EkartShippingService()
        else:
            self.shipping_service = DelhiveryShippingService()

    def process_order(self, item_name, packaging_type):
        if self.inventory_service.check_item(item_name):
            self.inventory_service.reserve_item(item_name)
            self.packaging_service.package_item(packaging_type)
            self.shipping_service.ship_item()

            """
            THIS IS WHERE we are checking if the service provides TRACKABLE AND ETA feature
            IN CASE OF DELHIVERY IT WILL show and in case of EKART it wont show!
            """
            if isinstance(self.shipping_service,Trackable):
                self.shipping_service.track_service()
            if isinstance(self.shipping_service,ETAChecker):
                self.shipping_service.eta_service()


            print("Order processed successfully")



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


if __name__ == "__main__":
    main()
