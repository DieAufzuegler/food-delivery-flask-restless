import unittest
import subprocess
import requests
import time

class MenuTest(unittest.TestCase):
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

    def test_get_menu(self):
        url = 'http://localhost:5000/api/restaurant/menu/1'
        request = requests.get(url, headers=self.defaultheaders)
        self.assertEqual(request.status_code, 200)
        #print(request.json())
        expected = {'id': 1, 'menu': {'address': 'Time Square 1, New New York', 'password': 'admin', 'email': 'panuccis@example.com', 'subscription_type': 'Display only', 'owner': 'Enzo Panucci', 'id': 1, 'name': 'Panuccis Pizza', 'menu_id': 1, 'phone': '+1 555 123456', 'username': 'donenzo'}, 'menu_items': [{'id': 1, 'price': 6.99, 'menu_id': 1, 'name': 'Pizza Margherita'}, {'id': 2, 'price': 7.99, 'menu_id': 1, 'name': 'Pizza Salami'}]}
        self.assertDictEqual(request.json(), expected)

    def test_add_menu_without_authorization(self):
        pass # TODO

    def test_add_menu_with_authorization(self):
        pass # TODO

    def test_update_menu_without_authorization(self):
        pass # TODO

    def test_update_menu_with_authorization(self):
        pass # TODO

    def test_delete_menu_without_authorization(self):
        pass # TODO

    def test_delete_menu_with_authorization(self):
        pass # TODO


if __name__ == '__main__':
    unittest.main()