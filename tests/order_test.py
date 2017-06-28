import unittest
import subprocess
import requests
import time

class OrderTest(unittest.TestCase):
    process = None
    socket = None
    defaultheaders = {'content-type': 'application/json'}
    authheaders = {'content-type': 'application/json', 'authorization': '0a21eccf0f7709bfc14fc90767e198f2'}
    
    def setUp(self):
        # start REST API server
        self.process = subprocess.Popen(['python3', '../app.py'],
                                        stdout=subprocess.DEVNULL,
                                        stderr=subprocess.DEVNULL)
        self.wait_for_server_to_fire_up()

    def tearDown(self):
        # send SIGTERM signal
        self.process.terminate()
        # wait for process to end
        self.process.wait() 

    def wait_for_server_to_fire_up(self):
        up = False
        while (not up):
            try:
                # try to rearch the server
                requests.get('http://localhost:5000/')
                # if no exception is thrown, server is up
                up = True
            except:
                # server is not up yet
                time.sleep(0.05)

    def helper_add_customer_and_authenticate(self):
        url = 'http://localhost:5000/api/customer'
        data = '''{ "username": "doedoe", "password": "securepw", "firstname": "John", "lastname": "Doe", "email": "jd@example.com", "phone": "+49 123 456789" }'''
        request = requests.post(url, data=data, headers=self.defaultheaders)
        url = 'http://localhost:5000/auth'
        data = '''{ "username": "doedoe", "password": "securepw" }'''
        request = requests.post(url, data=data, headers=self.defaultheaders)

    def test_add_order_without_authorization(self):
        self.helper_add_customer_and_authenticate()
        url = 'http://localhost:5000/api/order'
        data = '''{ "customer_id": 1, "delivery_address": "Schlossallee 1, 12345 Aachen", "restaurant_id": 1, "status": "open" }'''
        request = requests.post(url, data=data, headers=self.defaultheaders)
        self.assertEqual(request.status_code, 401)

    def test_add_order_with_authorization(self):
        self.helper_add_customer_and_authenticate()
        url = 'http://localhost:5000/api/order'
        data = '''{ "customer_id": 1, "delivery_address": "Schlossallee 1, 12345 Aachen", "restaurant_id": 1, "status": "open" }'''
        request = requests.post(url, data=data, headers=self.authheaders)
        self.assertEqual(request.status_code, 201)
        #print(request.json())
        response = request.json()
        del response['timestamp']
        expected = {'status': 'open', 'restaurant': {'phone': '+1 555 123456', 'owner': 'Enzo Panucci', 'email': 'panuccis@example.com', 'id': 1, 'address': 'Time Square 1, New New York', 'name': 'Panuccis Pizza', 'subscription_type': 'Display only', 'password': 'admin', 'menu_id': 1, 'username': 'donenzo'}, 'id': 1, 'delivery_address': 'Schlossallee 1, 12345 Aachen', 'restaurant_id': 1, 'customer': {'email': 'jd@example.com', 'id': 1, 'lastname': 'Doe', 'firstname': 'John', 'password': 'securepw', 'phone': '+49 123 456789', 'username': 'doedoe'}, 'customer_id': 1, 'deliveryperson_id': None, 'order_items': []}
        self.assertDictEqual(response, expected)

    def test_get_order_without_authorization(self):
        self.helper_add_customer_and_authenticate()
        url = 'http://localhost:5000/api/order'
        data = '''{ "customer_id": 1, "delivery_address": "Schlossallee 1, 12345 Aachen", "restaurant_id": 1, "status": "open" }'''
        request = requests.post(url, data=data, headers=self.defaultheaders)
        self.assertEqual(request.status_code, 401)

    def test_get_order_with_authorization(self):
        self.test_add_order_with_authorization()
        url = 'http://localhost:5000/api/order/1'
        request = requests.get(url, headers=self.authheaders)
        self.assertEqual(request.status_code, 200)
        #print(request.json())
        response = request.json()
        del response['timestamp']
        expected = {'order_items': [], 'customer': {'password': 'securepw', 'phone': '+49 123 456789', 'firstname': 'John', 'lastname': 'Doe', 'id': 1, 'username': 'doedoe', 'email': 'jd@example.com'}, 'status': 'open', 'restaurant_id': 1, 'deliveryperson_id': None, 'delivery_address': 'Schlossallee 1, 12345 Aachen', 'id': 1, 'restaurant': {'subscription_type': 'Display only', 'password': 'admin', 'owner': 'Enzo Panucci', 'menu_id': 1, 'address': 'Time Square 1, New New York', 'phone': '+1 555 123456', 'name': 'Panuccis Pizza', 'id': 1, 'username': 'donenzo', 'email': 'panuccis@example.com'}, 'customer_id': 1}
        self.assertDictEqual(response, expected)

    def test_update_order_without_authorization(self):
        pass # TODO

    def test_update_order_with_authorization(self):
        pass # TODO

    def test_delete_order(self):
        url = 'http://localhost:5000/api/order/42'
        request = requests.delete(url, headers=self.defaultheaders)
        self.assertEqual(request.status_code, 405)


if __name__ == '__main__':
    unittest.main()