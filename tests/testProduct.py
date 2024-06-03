import unittest
from unittest.mock import MagicMock, patch
from app import create_app
from faker import Faker

fake = Faker()

class TestProductsEndpoint(unittest.TestCase):
    def setUp(self):
        app = create_app('DevelopmentConfig')
        app.config['TESTING'] = True
        self.app = app.test_client()
    
    @patch('services.customerService.save')
    def test_create_customer(self, mock_save):
        name = fake.name()
        price = fake.random_number()
        mock_customer = MagicMock()
        mock_customer.id = 1
        mock_customer.name = name
        mock_customer.price = price

        mock_save.return_value = mock_customer

        payload = {
            "name": name,
            "price": price,
        }

        response = self.app.post('/products/', json=payload)

        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.json['id'], mock_customer.id)


    @patch('services.productService.save')
    def test_missing_price_payload(self, mock_save):
        name = fake.name()
        mock_customer = MagicMock()
        mock_customer.id = 1
        mock_customer.name = name
        mock_save.return_value = mock_customer

        payload = {
            "name": name,
        }

        response = self.app.post('/products/', json=payload)

        self.assertEqual(response.status_code, 400)
        self.assertIn('price', response.json)