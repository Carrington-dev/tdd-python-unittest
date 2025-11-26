import unittest
import logging
import sys
from shopping_cart import ShoppingCart

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/test_shopping_cart.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class TestShoppingCart(unittest.TestCase):
    def setUp(self):
        # Initialize a new ShoppingCart instance before each test
        self.cart = ShoppingCart()

    def tearDown(self):
        # Clean up after each test
        self.cart = None
    
    def test_add_item(self):
        self.cart.add_item("apple", 3)
        self.assertEqual(self.cart.view_cart(), [
            {
                'item': "apple",
                'quantity': 3,
                'price_per_unit': 1.0,
                'total_price': 3.0
            }
        ])
        self.cart.add_item("orange", 2)
        self.assertEqual(self.cart.view_cart(), [
            {
                'item': "apple",
                'quantity': 3,
                'price_per_unit': 1.0,
                'total_price': 3.0
            },
            {
                'item': "orange",
                'quantity': 2,
                'price_per_unit': 1.5,
                'total_price': 3.0
            }
        ])

    def test_remove_item(self):
        self.cart.add_item("banana", 2)
        self.cart.add_item("orange", 1)
        self.cart.remove_item("banana")
        self.assertEqual(self.cart.view_cart(), [
            {
                'item': "banana",
                'quantity': 1,
                'price_per_unit': 0.5,
                'total_price': 0.5
            },
            {
                'item': "orange",
                'quantity': 1,
                'price_per_unit': 1.5,
                'total_price': 1.5
            }
        ])

    def test_remove_item_to_empty(self):
        self.cart.add_item("grape", 1)
        self.cart.add_item("grape", 1)
        logger.info(
            f"Test remove_item_to_empty passed. cart.remove_item('grape') called twice. {self.cart.view_cart()}"
            )
        self.cart.remove_item("grape")
        self.cart.remove_item("grape")
        self.assertEqual(self.cart.view_cart(), [])

class TestShoppingCartLogging(unittest.TestCase):
    def setUp(self):
        # Initialize a new ShoppingCart instance before each test
        self.cart = ShoppingCart()
    
    def tearDown(self):
        # Clean up after each test
        self.cart = None

    def test_logging_on_add(self):
        with self.assertLogs('shopping_cart', level='INFO') as cm:
            self.cart.add_item("apple", 2)
            self.cart.add_item("banana", 3)
        
        self.assertIn("Added 2 of apple to cart.", cm.output[0])
        self.assertIn("Added 3 of banana to cart.", cm.output[1])

    def test_logging_on_remove(self):
        self.cart.add_item("orange", 2)
        with self.assertLogs('shopping_cart', level='INFO') as cm:
            self.cart.remove_item("orange")
            self.cart.remove_item("orange")
        
        self.assertIn("Updated orange quantity to 1.", cm.output[0])
        self.assertIn("Removed orange from cart.", cm.output[1])

    def test_logging_on_invalid_product_add(self):
        with self.assertLogs('shopping_cart', level='INFO') as cm:
            self.cart.add_item("kiwi", 1)
        
        self.assertIn("Product does not exist in catalog.", cm.output[0])

    def test_logging_on_invalid_product_remove(self):
        with self.assertLogs('shopping_cart', level='INFO') as cm:
            self.cart.remove_item("kiwi")
        
        self.assertIn("Product does not exist in catalog.", cm.output[0])