# How to write a testsuite
* see how testing is done in customer_test.py
* create a new file somthing_test.py
* copy the contents of customer_test.py to your newly created file
* remove customer related testcases (all methods starting with 'test_')
* make sure the methods setUp(), tearDown() and wait_for_server_to_fire_up() are still there
* write your own testcases. Stick to the naming convention test_something
* run your tests with the command ```python3 something_test.py```
* edit testsuite.py. Import your test class and add your class to the 'test_classes_to_run' array
* run the entire test suite with the command ```python3 testsuite.py```

# How to know what to expect
Some testcases use a Python dictionary called "expected" to make an assertDictEqual.
If you are not sure what the "expected" dictionary should look like, temporarily add the following line to your testcase just after making the request
> print(request.json())  

run the test and simply copy and paste the output 
