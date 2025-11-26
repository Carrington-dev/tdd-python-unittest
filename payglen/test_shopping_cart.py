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

    def test_total_cart_price(self):
        self.cart.add_item("apple", 2)  # 2 * 1.0 = 2.0
        self.cart.add_item("banana", 4) # 4 * 0.5 = 2.0
        self.cart.add_item("orange", 1) # 1 * 1.5 = 1.5
        total = self.cart.get_total_price()
        self.assertEqual(total, 5.5)  # Total should be 2.0 + 2.0 + 1.5 = 5.5

    def test_view_cart(self):
        self.cart.add_item("apple", 1)
        self.cart.add_item("banana", 2)
        expected_view = [
            {
                'item': "apple",
                'quantity': 1,
                'price_per_unit': 1.0,
                'total_price': 1.0
            },
            {
                'item': "banana",
                'quantity': 2,
                'price_per_unit': 0.5,
                'total_price': 1.0
            }
        ]
        self.assertEqual(self.cart.view_cart(), expected_view)

    def test_add_invalid_product(self):
        self.cart.add_item("kiwi", 1)  # kiwi is not in the product catalog
        self.assertEqual(self.cart.view_cart(), [])  # Cart should remain empty
    
    def test_remove_invalid_product(self):
        self.cart.add_item("apple", 1)
        self.cart.remove_item("kiwi")  # kiwi is not in the product catalog
        expected_view = [
            {
                'item': "apple",
                'quantity': 1,
                'price_per_unit': 1.0,
                'total_price': 1.0
            }
        ]
        self.assertEqual(self.cart.view_cart(), expected_view)  # Cart should remain unchanged

    def test_total_item_count(self):
        self.cart.add_item("apple", 2)
        self.cart.add_item("banana", 3)
        total_items = self.cart.get_total()
        self.assertEqual(total_items, 5)  # 2 apples + 3 bananas = 5 items

    def test_total_item_count_empty_cart(self):
        total_items = self.cart.get_total()
        self.assertEqual(total_items, 0)  # Empty cart should have 0 items

    def test_total_item_count_after_removals(self):
        self.cart.add_item("orange", 4)
        self.cart.remove_item("orange")
        total_items = self.cart.get_total()
        self.assertEqual(total_items, 3)  # 4 - 1 = 3 oranges left

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