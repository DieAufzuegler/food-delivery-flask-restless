import unittest
from generic_test import GenericTest 
from customer_test import CustomerTest
from deliveryperson_test import DeliveryPersonTest
from order_test import OrderTest
from restaurant_test import RestaurantTest


if __name__ == '__main__':
    test_classes_to_run = [GenericTest, CustomerTest, DeliveryPersonTest, OrderTest, RestaurantTest]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
