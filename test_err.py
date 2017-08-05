import sys
from err import ErrCls
from test_suite import good
errors = ErrCls(testing = True, debug = True)
# TODO Somehow need to determine if deepsleep() was called. Maybe a
# wrapper?

test_message = "Test message"

errors.warn(test_message)
print("errors.log: '" + str(errors.log) + "'")
# FIXME Actually it's '[(146, 'warning', {'message': 'Test message'})]'
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
    test_message['exc_type'] = str(sys.exc_info()[0])
    test_message['error'] = str(sys.exc_info()[1]).strip()
    errors.exc(test_message)

assert test_message in errors.log, "errors.exc()"
good("errors.exc()")

errors.log = list()