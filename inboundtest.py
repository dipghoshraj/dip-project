import unittest
import json
from app import app

class TestInboundSMSAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.valid_credentials = 'Basic YXpyMToyMFMwS1BOT0lN'  # Replace with your valid credentials

    def test_inbound_sms_missing_parameters(self):
        response = self.app.post('/inbound/sms/', headers={'Authorization': self.valid_credentials}, data=json.dumps({}), content_type='application/json')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertIn('message', data)
        self.assertIn('error', data)
        self.assertEqual(data['message'], '')
        self.assertIn('is missing', data['error'])

    def test_inbound_sms_invalid_parameters(self):
        data = {
            'form': '12345',  # Invalid 'form' parameter
            'to': 'unknown_number', #invalid 'to' parameter
            'text': 'Hello World'
        }

        response = self.app.post('/inbound/sms/', headers={'Authorization': self.valid_credentials}, data=json.dumps(data), content_type='application/json')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertIn('message', data)
        self.assertIn('error', data)
        self.assertEqual(data['message'], '')
        self.assertIn('is invalid', data['error'])

    def test_inbound_sms_to_not_found(self):
        data = {
            'form': '91983435345',
            'to': '1234567890',  # 'to' not found in the phone_number table
            'text': 'Hello World'
        }

        response = self.app.post('/inbound/sms/', headers={'Authorization': self.valid_credentials}, data=json.dumps(data), content_type='application/json')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertIn('message', data)
        self.assertIn('error', data)
        self.assertEqual(data['message'], '')
        self.assertIn('to parameter not found', data['error'])

    def test_inbound_sms_successful(self):
        data = {
            'form': '91983435345',
            'to': '4924195509196',
            'text': 'Hello World'
        }

        response = self.app.post('/inbound/sms/', headers={'Authorization': self.valid_credentials}, data=json.dumps(data), content_type='application/json')
        print(" response data is ", response.status_code)
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        self.assertIn('error', data)
        self.assertEqual(data['message'], 'inbound sms ok')
        self.assertEqual(data['error'], '')

if __name__ == '__main__':
    unittest.main()
