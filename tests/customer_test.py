import unittest
import subprocess
import requests
import time

class CustomerTest(unittest.TestCase):
    process = None
    socket = None
    headers = {'content-type': 'application/json'}
    
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
    
    def test_add_customer(self):
        url = 'http://localhost:5000/api/customer'
        data = '''{ "username": "doedoe", "password": "securepw", "firstname": "John", "lastname": "Doe", "email": "jd@example.com", "phone": "+49 123 456789" }'''
        request = requests.post(url, data=data, headers=self.headers)
        self.assertEqual(request.status_code, 201)
        #print(request.json())
        expected = {'lastname': 'Doe', 'id': 1, 'phone': '+49 123 456789', 'firstname': 'John', 'username': 'doedoe', 'email': 'jd@example.com', 'order': None}
        self.assertDictEqual(request.json(), expected)

    def test_authenticate_non_existing_customer(self):
        url = 'http://localhost:5000/auth'
        data = '''{ "username": "derpy", "password": "schuesch" }'''
        request = requests.post(url, data=data, headers=self.headers)
        self.assertEqual(request.status_code, 401)

    def test_authenticate_existing_customer(self):
        self.test_add_customer() # reuse previous test that adds customer
        url = 'http://localhost:5000/auth'
        data = '''{ "username": "doedoe", "password": "securepw" }'''
        request = requests.post(url, data=data, headers=self.headers)
        self.assertEqual(request.status_code, 200)
        #print(request.json())
        expected = {'token': '0a21eccf0f7709bfc14fc90767e198f2'}
        self.assertDictEqual(request.json(), expected)

    def test_get_customer_without_authorization(self):
        url = 'http://localhost:5000/api/customer/1'
        request = requests.get(url, headers=self.headers)
        self.assertEqual(request.status_code, 401)

    def test_get_customer_with_authorization(self):
        self.test_authenticate_existing_customer() # reuse previous test to add and authenticate customer
        url = 'http://localhost:5000/api/customer/1'
        customheaders = {'content-type': 'application/json', 'authorization': '0a21eccf0f7709bfc14fc90767e198f2'}
        request = requests.get(url, headers=customheaders)
        self.assertEqual(request.status_code, 200)
        #print(request.json())
        expected = {'email': 'jd@example.com', 'order': None, 'lastname': 'Doe', 'username': 'doedoe', 'phone': '+49 123 456789', 'id': 1, 'firstname': 'John'}
        self.assertDictEqual(request.json(), expected)

    def test_delete_customer_without_authorization(self):
        self.test_add_customer() # reuse previous test that adds customer
        url = 'http://localhost:5000/api/customer/1'
        request = requests.delete(url, headers=self.headers)
        self.assertEqual(request.status_code, 401)
    
    def test_delete_customer_with_authorization(self):
        self.test_authenticate_existing_customer() # reuse previous test to add and authenticate customer
        url = 'http://localhost:5000/api/customer/1'
        customheaders = {'content-type': 'application/json', 'authorization': '0a21eccf0f7709bfc14fc90767e198f2'}
        request = requests.delete(url, headers=customheaders)
        self.assertEqual(request.status_code, 204)

    def test_update_customer_without_authorization(self):
        self.test_authenticate_existing_customer() # reuse previous test to add and authenticate customer
        url = 'http://localhost:5000/api/customer/1'
        data = '''{ "phone": "555-987461" }'''
        request = requests.put(url, data=data, headers=self.headers)
        self.assertEqual(request.status_code, 401)
    
    def test_update_customer_with_authorization(self):
        self.test_authenticate_existing_customer() # reuse previous test to add and authenticate customer
        url = 'http://localhost:5000/api/customer/1'
        data = '''{ "phone": "555-987461" }'''
        customheaders = {'content-type': 'application/json', 'authorization': '0a21eccf0f7709bfc14fc90767e198f2'}
        request = requests.put(url, data=data, headers=customheaders)
        self.assertEqual(request.status_code, 200)
        #print(request.json())
        expected = {'username': 'doedoe', 'phone': '555-987461', 'order': None, 'lastname': 'Doe', 'firstname': 'John', 'id': 1, 'email': 'jd@example.com'}
        self.assertDictEqual(request.json(), expected)



if __name__ == '__main__':
    unittest.main()