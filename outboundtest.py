import unittest
import json
from app import app

class TestOutboundSMSAPI(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.valid_credentials = 'Basic YXpyMToyMFMwS1BOT0lN'
    def test_outbound_sms_missing_parameters(self):
        response = self.app.post('/outbound/sms/', headers={'Authorization': self.valid_credentials}, data=json.dumps({}), content_type='application/json')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertIn('message', data)
        self.assertIn('error', data)
        self.assertEqual(data['message'], '')
        self.assertIn('is missing', data['error'])

    def test_outbound_sms_invalid_parameters(self):
        data = {
            'form': '123',
            'to': '919343542749',
            'text': 'hello from plivo Auzmor'
        }

        response = self.app.post('/outbound/sms/', headers={'Authorization': self.valid_credentials}, data=json.dumps(data), content_type='application/json')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertIn('message', data)
        self.assertIn('error', data)
        self.assertEqual(data['message'], '')
        self.assertIn('is invalid', data['error'])

    def test_outbound_sms_blocked_by_stop_request(self):
        data = {
            'form': '4924195509196',
            'to': '91983435345',
            'text': 'hello from plivo Auzmor'
        }

        response = self.app.post('/outbound/sms/', headers={'Authorization': self.valid_credentials}, data=json.dumps(data), content_type='application/json')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertIn('message', data)
        self.assertIn('error', data)
        self.assertEqual(data['message'], '')
        self.assertIn('sms from 4924195509196 to 91983435345 blocked by STOP request', data['error'])

    def test_outbound_sms_from_not_found(self):
        data = {
            'form': '123456789',
            'to': '919343542749',
            'text': 'hello from plivo Auzmor'
        }

        response = self.app.post('/outbound/sms/', headers={'Authorization': self.valid_credentials}, data=json.dumps(data), content_type='application/json')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertIn('message', data)
        self.assertIn('error', data)
        self.assertEqual(data['message'], '')
        self.assertIn('from parameter not found', data['error'])

    def test_outbound_sms_limit_reached(self):
        # to test this we need to modify the redis counter or by changing the reate limit in the api_call_limit decorator
        data = {
            'form': '3253280312',
            'to': '919343542749',
            'text': 'hello from plivo Auzmor'
        }

        response = self.app.post('/outbound/sms/', headers={'Authorization': self.valid_credentials}, data=json.dumps(data), content_type='application/json')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertIn('message', data)
        self.assertIn('error', data)
        self.assertEqual(data['message'], '')
        self.assertIn('limit reached for from 3253280312', data['error'])

    def test_outbound_sms_successful(self):
        data = {
            "form": "4924195509196",
            "to": "91983435346",
            "text": "Hello World"
        }

        response = self.app.post('/outbound/sms/', headers={'Authorization': self.valid_credentials}, data=json.dumps(data), content_type='application/json')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        self.assertIn('error', data)
        self.assertEqual(data['message'], 'outbound sms ok')
        self.assertEqual(data['error'], '')

if __name__ == '__main__':
    unittest.main()
