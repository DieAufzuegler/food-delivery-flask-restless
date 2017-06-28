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


if __name__ == '__main__':
    unittest.main()