import unittest
from unittest.mock import MagicMock, patch
from app import create_app
from faker import Faker

fake = Faker()

class TestCustomersEndpoint(unittest.TestCase):
    def setUp(self):
        app = create_app('DevelopmentConfig')
        app.config['TESTING'] = True
        self.app = app.test_client()
    
    @patch('services.customerService.save')
    def test_create_customer(self, mock_save):
        name = fake.name()
        phone = fake.phone_number()
        email = fake.email()
        mock_customer = MagicMock()
        mock_customer.id = 1
        mock_customer.name = name
        mock_customer.phone = phone
        mock_customer.email = email
        mock_save.return_value = mock_customer

        payload = {
            "name": name,
            "phone": phone,
            "email": email,
        }

        response = self.app.post('/customers/', json=payload)

        self.assertEquals(response.status_code, 201)
        self.assertEquals(response.json['id'], mock_customer.id)


    @patch('services.customerService.save')
    def test_missing_phone_payload(self, mock_save):
        name = fake.name()
        email = fake.email()
        mock_customer = MagicMock()
        mock_customer.id = 1
        mock_customer.name = name
        mock_customer.email = email
        mock_save.return_value = mock_customer

        payload = {
            "name": name,
            "email": email,
        }

        response = self.app.post('/customers/', json=payload)

        self.assertEqual(response.status_code, 400)
        self.assertIn('phone', response.json)