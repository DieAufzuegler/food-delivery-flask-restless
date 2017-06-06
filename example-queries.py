import argparse
import subprocess
from time import sleep
from random import random

def faketype(string):
    for s in string:
        print(s, end='', flush=True)
        sleep(random()*0.03)

commands = [
    ['List all restaurants', 'curl -H "Content-Type: application/json" -i http://localhost:5000/api/restaurant' ],
    #['Add restaurant Panuccis Pizza', 'curl -H "Content-Type: application/json" -i -X POST -d \'{ "username": "donenzo", "name": "Panuccis Pizza", "address": "Time Square 1, New New York", "owner": "Enzo Panucci", "email": "panuccis@example.com", "phone": "+1 555 123456", "subscription_type": "Display only" }\' http://localhost:5000/api/restaurant'],
    #['Add another restaurant', 'curl -H "Content-Type: application/json" -i -X POST -d \'{ "username": "veganpower", "name": "Hipster Hut", "address": "Somewhere", "owner": "Ernst Freigeist", "email": "veganpower@example.com", "phone": "+49 213 12321", "subscription_type": "Premium" }\' http://localhost:5000/api/restaurant'],
    #['List all restaurants again', 'curl -H "Content-Type: application/json" -i http://localhost:5000/api/restaurant' ],
    ['Add customer John Doe', 'curl -H "Content-Type: application/json" -i -X POST -d \'{ "username": "doedoe", "firstname": "John", "lastname": "Doe", "email": "jd@example.com", "phone": "+49 123 456789" }\' http://localhost:5000/api/customer'],
    ['Get customer with ID 1', 'curl -H "Content-Type: application/json" -i http://localhost:5000/api/customer/1'],
    ['John Doe places an order at Panuccis Pizza', 'curl -H "Content-Type: application/json" -i -X POST -d \'{ "customer_id": 1, "delivery_address": "Schlossallee 1, 12345 Aachen", "restaurant_id": 1, "status": "open }\' http://localhost:5000/api/order'],
    #['Get order with ID 1', 'curl -H "Content-Type: application/json" -i http://localhost:5000/api/order/1'],
    ['Add delivery person', 'curl -H "Content-Type: application/json" -i -X POST -d \'{ "username": "hermes", "firstname": "Hermes", "lastname": "Konrad", "email": "hermes@example.com", "phone": "+49 123 456789" }\' http://localhost:5000/api/deliveryperson'],
    ['Assign John Doe\'s order placed with Panuccis Pizza to this delivery person', 'curl -H "Content-Type: application/json" -i -X PUT -d \'{ "on_duty": true, "has_order_assigned": true, "assigned_order": 1 }\' http://localhost:5000/api/deliveryperson/1'],
    ['Get delivery person with ID 1', 'curl -H "Content-Type: application/json" -i http://localhost:5000/api/deliveryperson/1'],
    ['Get customer with ID 1', 'curl -H "Content-Type: application/json" -i http://localhost:5000/api/customer/1'],
]

parser = argparse.ArgumentParser(description='Sends a couple of queries to the REST API for demo purposes.')
parser.add_argument('-q', '--quick', action='store_true', help='Don\'t "fake type" the curl commands')
args = parser.parse_args()

for command in commands:
    # clear screen
    subprocess.run("clear", shell=True)

    # print command description
    print("\033[1m" + command[0] + "\033[0m\n")

    # fake type command into console and wait for user to hit enter
    if args.quick:
        print("$ " + command[1], end='')
    else:
        print("$ ", end='')
        faketype(command[1])
    input()

    # run the command
    print()
    subprocess.run(command[1], shell=True)
    input()
    