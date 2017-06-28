import unittest
import subprocess
import requests
import time

class GenericTest(unittest.TestCase):
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

    def test_REST_API_process_is_running(self):
        self.assertIsNone(self.process.poll())
    
    def test_content_type(self):
        url = 'http://localhost:5000/api/restaurant'
        request = requests.get(url, headers=self.headers)
        self.assertEqual(request.headers['content-type'], 'application/json, application/json')
    
    def test_hardcoded_data(self):
        url = 'http://localhost:5000/api/restaurant'
        request = requests.get(url, headers=self.headers)
        expected = {'total_pages': 1, 'num_results': 2, 'objects': [{'subscription_type': 'Display only', 'orders': [], 'menu': {'id': 1}, 'menu_id': 1, 'address': 'Time Square 1, New New York', 'owner': 'Enzo Panucci', 'phone': '+1 555 123456', 'name': 'Panuccis Pizza', 'email': 'panuccis@example.com', 'username': 'donenzo', 'id': 1}, {'subscription_type': 'Premium', 'orders': [], 'menu': None, 'menu_id': None, 'address': 'Somewhere', 'owner': 'Ernst Freigeist', 'phone': '+49 213 12321', 'name': 'Hipster Hut', 'email': 'veganpower@example.com', 'username': 'veganpower', 'id': 2}], 'page': 1}
        self.assertDictEqual(request.json(), expected)


if __name__ == '__main__':
    unittest.main()