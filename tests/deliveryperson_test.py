import unittest
import subprocess
import requests
import time

class DeliveryPersonTest(unittest.TestCase):
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
    
    def test_add_deliveryperson(self):
        url = 'http://localhost:5000/api/deliveryperson'
        data = '''{ "username": "hermes", "password": "securepw", "firstname": "Hermes", "lastname": "Konrad", "email": "hermes@example.com", "phone": "+49 123 456789" }'''
        request = requests.post(url, data=data, headers=self.headers)
        self.assertEqual(request.status_code, 201)
        #print(request.json())
        expected = {'lastname': 'Konrad', 'on_duty': False, 'username': 'hermes', 'phone': '+49 123 456789', 'assigned_order': [], 'firstname': 'Hermes', 'email': 'hermes@example.com', 'id': 1}
        self.assertDictEqual(request.json(), expected)

    def test_authenticate_non_existing_deliveryperson(self):
        url = 'http://localhost:5000/auth'
        data = '''{ "username": "derpy", "password": "schuesch" }'''
        request = requests.post(url, data=data, headers=self.headers)
        self.assertEqual(request.status_code, 401)

    def test_authenticate_existing_deliveryperson(self):
        self.test_add_deliveryperson() # reuse previous test that adds deliveryperson
        url = 'http://localhost:5000/auth'
        data = '''{ "username": "hermes", "password": "securepw" }'''
        request = requests.post(url, data=data, headers=self.headers)
        self.assertEqual(request.status_code, 200)
        #print(request.json())
        expected = {'token': '0a21eccf0f7709bfc14fc90767e198f2'}
        self.assertDictEqual(request.json(), expected)

    def test_get_deliveryperson_without_authorization(self):
        url = 'http://localhost:5000/api/deliveryperson/1'
        request = requests.get(url, headers=self.headers)
        self.assertEqual(request.status_code, 401)

    def test_get_deliveryperson_with_authorization(self):
        self.test_authenticate_existing_deliveryperson() # reuse previous test to add and authenticate deliveryperson
        url = 'http://localhost:5000/api/deliveryperson/1'
        customheaders = {'content-type': 'application/json', 'authorization': '0a21eccf0f7709bfc14fc90767e198f2'}
        request = requests.get(url, headers=customheaders)
        self.assertEqual(request.status_code, 200)
        #print(request.json())
        expected = {'assigned_order': [], 'on_duty': False, 'id': 1, 'firstname': 'Hermes', 'phone': '+49 123 456789', 'email': 'hermes@example.com', 'username': 'hermes', 'lastname': 'Konrad'}
        self.assertDictEqual(request.json(), expected)

    def test_delete_deliveryperson_without_authorization(self):
        return
        self.test_add_deliveryperson() # reuse previous test that adds deliveryperson
        url = 'http://localhost:5000/api/deliveryperson/1'
        request = requests.delete(url, headers=self.headers)
        self.assertEqual(request.status_code, 401)
    
    def test_delete_deliveryperson_with_authorization(self):
        self.test_authenticate_existing_deliveryperson() # reuse previous test to add and authenticate deliveryperson
        url = 'http://localhost:5000/api/deliveryperson/1'
        customheaders = {'content-type': 'application/json', 'authorization': '0a21eccf0f7709bfc14fc90767e198f2'}
        request = requests.delete(url, headers=customheaders)
        self.assertEqual(request.status_code, 204)

    def test_update_deliveryperson_without_authorization(self):
        self.test_authenticate_existing_deliveryperson() # reuse previous test to add and authenticate deliveryperson
        url = 'http://localhost:5000/api/deliveryperson/1'
        data = '''{ "phone": "555-987461" }'''
        request = requests.put(url, data=data, headers=self.headers)
        self.assertEqual(request.status_code, 401)
    
    def test_update_deliveryperson_with_authorization(self):
        self.test_authenticate_existing_deliveryperson() # reuse previous test to add and authenticate deliveryperson
        url = 'http://localhost:5000/api/deliveryperson/1'
        data = '''{ "phone": "555-987461" }'''
        customheaders = {'content-type': 'application/json', 'authorization': '0a21eccf0f7709bfc14fc90767e198f2'}
        request = requests.put(url, data=data, headers=customheaders)
        self.assertEqual(request.status_code, 200)
        #print(request.json())
        expected = {'firstname': 'Hermes', 'phone': '555-987461', 'id': 1, 'lastname': 'Konrad', 'assigned_order': [], 'email': 'hermes@example.com', 'username': 'hermes', 'on_duty': False}
        self.assertDictEqual(request.json(), expected)


if __name__ == '__main__':
    unittest.main()