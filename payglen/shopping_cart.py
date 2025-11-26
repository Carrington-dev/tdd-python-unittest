import logging

logger = logging.getLogger(__name__)

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"Product(name={self.name}, price={self.price})"

products = {
    "apple": Product("apple", 1.0),
    "banana": Product("banana", 0.5),
    "orange": Product("orange", 1.5),
    "grape": Product("grape", 2.0),
}

class ShoppingCart:
    def __init__(self):
        self._items = {

        }  
        self._products = products
    
    def add_item(self, item_name, quantity):
        if item_name in self._products:

            if item_name not in self._items:
                self._items[item_name] = {
                    'product': self._products.get(item_name), 
                    'quantity': quantity
                    }
                logger.info(f"Added {quantity} of {item_name} to cart.")
            else:
                self._items[item_name]['quantity'] += quantity
                logger.info(f"Updated {item_name} quantity to {self._items[item_name]['quantity']}.")
        else:
            logger.info(f"Product does not exist in catalog.")   

    def remove_item(self, item_name):
        if item_name in self._products:
            if item_name not in self._items:
                pass
            else:
                self._items[item_name]['quantity'] -= 1
                if self._items[item_name]['quantity'] <= 0:
                    del self._items[item_name]
                    logger.info(f"Removed {item_name} from cart.")
                else:   
                    logger.info(f"Updated {item_name} quantity to {self._items[item_name]['quantity']}.")
        else:
            logger.info(f"Product does not exist in catalog.")   

    def get_total_price(self):
        total = sum(item["quantity"] * item["product"].price for item in self._items.values())
        return total

    def get_total(self):
        total = sum(item["quantity"] for item in self._items.values())
        return total
    
    def view_cart(self):
        return [
            {
                'item': item_name,
                'quantity': item_info['quantity'],
                'price_per_unit': item_info['product'].price,
                'total_price': item_info['quantity'] * item_info['product'].price
            }
            for item_name, item_info in self._items.items()
        ]

    def value_added_tax(self, tax_rate = 0.15):
        total = self.get_total()
        vat = total * tax_rate
        return vat

if __name__ == "__main__":
    cart = ShoppingCart()
    cart.add_item("apple", 2)
    cart.add_item("banana", 3)
    print("Cart contents:", cart.view_cart())
    cart.remove_item("apple")
    print("Cart contents after removal:", cart.view_cart())
    total = cart.get_total()
    print("Total cart value:", total)
