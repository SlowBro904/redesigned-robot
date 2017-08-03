from err import ErrCls
from test_suite import good
errors = ErrCls(testing = True, debug = True)
# FIXME Load the data_store and ensure the data got saved.
# TODO Also somehow need to determine if deepsleep() was called. Maybe a
# wrapper?

test_message = "Test message"

errors.warn(test_message)
assert test_message in errors.log, "errors.warn()"
good("errors.warn()")

# Clear the log
errors.log = list()

errors.err(test_message)
assert test_message in errors.log, "errors.err()"
good("errors.err()")

try:
    raise RuntimeError("errors.exc()")
except RuntimeError:
    test_message = {'file': __file__, 'func': __name__,
                    'action': "Testing exception logging"}
    errors.exc(test_message)

# FIXME This probably will fail because exc() adds two more log parameters. Get
# those manually and add here.
assert test_message in errors.log, "errors.exc()"
good("errors.exc()")

errors.log = list()