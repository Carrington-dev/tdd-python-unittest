import logging
from shopping_cart import ShoppingCart

import unittest
import logging
import sys

# Configure logging for tests
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/test_shopping_cart_results.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)



class TestShoppingCart:
    def test_add_item(self):
        cart = ShoppingCart()
        cart.add_item("apple", 2)
        cart.add_item("banana", 3)
        assert cart.view_cart() == [
            {
                'item': 'apple', 
                'quantity': 2, 
                'price_per_unit': 1.0,
                'total_price': 2.0
                
            },
            {
                'item': 'banana', 
                'quantity': 3, 
                'price_per_unit': 0.5,
                'total_price': 1.5
            }
        ]

    def test_remove_item(self):
        cart = ShoppingCart()
        cart.add_item("orange", 2)
        cart.remove_item("orange")
        assert cart.view_cart() == [
            {
                'item': 'orange', 
                'quantity': 1, 
                'price_per_unit': 1.5,
                'total_price': 1.5
            }
        ]
        cart.remove_item("orange")
        assert cart.view_cart() == []
        logger.info("Test remove_item passed.")

class TestShoppingCartLogging(unittest.TestCase):
    def test_logging_on_add(self):
        cart = ShoppingCart()
        with self.assertLogs('shopping_cart', level='INFO') as cm:
            cart.add_item("grape", 1)
        self.assertIn("Added 1 of grape to cart.", cm.output[0])

    def test_logging_on_remove(self):
        cart = ShoppingCart()
        cart.add_item("grape", 1)
        with self.assertLogs('shopping_cart', level='INFO') as cm:
            cart.remove_item("grape")
        self.assertIn("Removed grape from cart.", cm.output[0])

if __name__ == "__main__":
    # test_cart = TestShoppingCart()
    # test_cart.test_add_item()
    # logger.info("Test add_item passed.")

    # test_cart.test_remove_item()
    test_shopping_cart_logging = TestShoppingCartLogging()
    test_shopping_cart_logging.test_logging_on_add()
    test_shopping_cart_logging.test_logging_on_remove()
    print("All tests passed.")