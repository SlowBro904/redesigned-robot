from err import Err
errors = Err()
# FIXME Test all three types by clearing the log, running them then compare the
# log to what was passed. Clear the log and try the next type. Finally, load
# the data_store and ensure the data got saved. We will need testing and debug
# flags. Also somehow need to measure when there is a reaction such as
# LEDs or deepsleep()