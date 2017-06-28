import unittest
from generic_test import GenericTest 
from customer_test import CustomerTest


if __name__ == '__main__':
    test_classes_to_run = [GenericTest, CustomerTest]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
