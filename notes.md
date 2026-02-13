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