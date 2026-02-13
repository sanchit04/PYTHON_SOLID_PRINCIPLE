from abc import ABC, abstractmethod


# =========================
# INVENTORY RESPONSIBILITY
# =========================
"""
AS PART OF DEPENDENCY INVERSION PRINCIPLE Inventory service is converted to ABC
So that any new Inventory can be supported in future also helps in OCP (Open Closed Principle)
"""
class InventoryService(ABC):
    @abstractmethod
    def check_item(self,item_name):
        pass

    @abstractmethod
    def reserve_item(self,item_name):
        pass

"""
Created a default implementation
"""
class DefaultInventoryService(InventoryService):
    def check_item(self, item_name):
        print(f"Checking inventory for {item_name}")
        return True

    def reserve_item(self, item_name):
        print(f"Reserving {item_name} from inventory")


# =========================
# PACKAGING RESPONSIBILITY
# =========================
"""
AS PART OF DEPENDENCY INVERSION PRINCIPLE PackagingService is converted to ABC
So that any new Inventory can be supported in future also helps in OCP (Open Closed Principle)
"""

class PackagingService(ABC):
    @abstractmethod
    def package_item(self,packaging_type):
        pass

"""
In this case liskov substitution is not violated since parent commits that item will be packaged
and the child even in if else case does packaging as per commitment from parent
This may violate open close in future for eg if DefaultPackaging now needs to add one more packaging type
eg carboncopy packaging type then in that case in this case we should seperate packagingType
class DefaultPackagingService(PackagingService):
    def package_item(self, packaging_type):
        if packaging_type == "GIFT":
            print("Using gift wrap")
            print("Adding greeting card")
        else:
            print("Using normal wrap")

will change to

class GiftPackagingService(PackagingService):
    def packaging_item(self):
        print("Using gift wrap")
        print("Adding greeting card")

class NormalPackagingService(PackagingService):
    def packaging_item(self):
        print("Using normal wrap")
        
class WoodenPackagingService(PackagingService):
    def packaging_item(self):
        print("Using wooden packaging")

"""
class DefaultPackagingService(PackagingService):
    def package_item(self, packaging_type):
        if packaging_type == "GIFT":
            print("Using gift wrap")
            print("Adding greeting card")
        else:
            print("Using normal wrap")


# =========================
# SHIPPING ABSTRACTION
# =========================


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

"""
In this case OrderService is directly creating objects of 
InventoryService, PackagingService, EkartShippingService, DelhiveryShippingService
In future if theres a new shipping server service or a different inventory service comes into picture
we will have to modify this code to point to the new one 
this is direct violation of Dependency inversion thus we need to change it to accept objects from parameters
and point to abstract base classes so that even if tomorrow any new service is introduced 
there will be no change in orderservice

PROBLEM:

    def __init__(self, category):
        self.inventory_service = InventoryService()
        self.packaging_service = PackagingService()

        if category == "ULTRA_EXPENSIVE":
            self.shipping_service = EkartShippingService()
        else:
            self.shipping_service = DelhiveryShippingService()
            
FIX 

Get the objects as parameter of abstract base class
InventoryService and PackagingService need to create ABCs
"""
class OrderService:
    # We are now injecting ABCs as object derived by main method
    # Thus making OrderService completely independent
    # of any changes to Inventory, Packaging or Shipping
    def __init__(self, inventory_service:InventoryService,
                 packaging_service:PackagingService,
                 shipping_service: ShippingService
                 ):
        self.inventory_service = inventory_service
        self. packaging_service = packaging_service
        self.shipping_service = shipping_service

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

    # NOW since order shipping service is totally independent of objects which are passed to it
    # which shipping service to be used moves to MAIN method (which is not ideal for PROD CODE)
    # But thats how it is at this point
    category = "LOW_EXPENSIVE"

    inventory_service = DefaultInventoryService()
    packaging_service = DefaultPackagingService()
    """
    To remove business rule from main:
    → Introduce a Factory (or Registry-based Factory) (Its a design pattern covered in later part)
    → Let it decide shipping
    → Keep main as composition root only
    """
    if category == "ULTRA_EXPENSIVE":
        shipping_service = EkartShippingService()
    else:
        shipping_service = DelhiveryShippingService()


    order_service = OrderService(inventory_service,packaging_service,shipping_service)

    order_service.process_order(
        item_name="iPhone 16",
        packaging_type="NORMAL"
    )


if __name__ == "__main__":
    main()
