import unittest
from unittest.mock import MagicMock, patch
from app import create_app
from faker import Faker

fake = Faker()

class TestOrdersEndpoint(unittest.TestCase):
    def setUp(self):
        app = create_app('DevelopmentConfig')
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch('services.orderService.save')
    def test_create_order(self, mock_save):
        customer_id = fake.random_number()
        product_id = fake.random_number()
        quantity = fake.random_number()
        total = fake.pyfloat()
        mock_order = MagicMock()
        mock_order.id = 1
        mock_order.customer_id = customer_id
        mock_order.product_id = product_id
        mock_order.quantity = quantity
        mock_order.total = total
        mock_save.return_value = mock_order

        total = {
                "customer_id": customer_id,
                "product_id": product_id,
                "quantity": quantity,
                "total": total
            }
        
        response = self.app.post('/orders/', json=total)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['id'], mock_order.id)

    @patch('services.orderService.save')
    def test_missing_quantity_total(self, mock_save):
        customer_id = fake.random_number()
        product_id = fake.random_number()
        total = fake.pyfloat()
        mock_order = MagicMock()
        mock_order.id = 1
        mock_order.customer_id = customer_id
        mock_order.product_id = product_id
        mock_order.total = total
        mock_save.return_value = mock_order

        total = {
                "customer_id": customer_id,
                "product_id": product_id,
                "total": total
            }

        response = self.app.post('/orders/', json=total)

        self.assertEqual(response.status_code, 400)
        self.assertIn('quantity', response.json)
