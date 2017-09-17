print("Starting test_deepsleep")
from test_suite import good
from deepsleep import deepsleep

check = 'deepsleep()'
print("This should print below ")
print("'[DEBUG] Simulating deep sleep of indefinite length.'")
deepsleep()

check = 'deepsleep(1)'
print("This should print below ")
print("'[DEBUG] Simulating deep sleep of 1 seconds.'")
deepsleep(1)