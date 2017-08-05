import sys
from err import ErrCls
from test_suite import good
errors = ErrCls(testing = True, debug = True)
# TODO Somehow need to determine if deepsleep() was called. Maybe a
# wrapper?

test_message = "Test message"

errors.warn(test_message)
found = False
if len(errors.log) > 0:
    for entry in errors.log:
        if len(entry) > 0:
            if entry[1] == 'warning':
                if 'message' in entry[2]:
                    if entry[2]['message'] == test_message:
                        found = True
                        break

assert found is True, "errors.warn()"
good("errors.warn()")

errors.err(test_message)
found = False
if len(errors.log) > 0:
    for entry in errors.log:
        if len(entry) > 0:
            if entry[1] == 'error':
                if 'message' in entry[2]:
                    if entry[2]['message'] == test_message:
                        found = True
                        break

assert found is True, "errors.err()"
good("errors.err()")

try:
    raise RuntimeError("errors.exc()")
except RuntimeError:
    test_message = {'file': __file__, 'func': __name__,
                    'action': "Testing exception logging"}
    test_message['exc_type'] = str(sys.exc_info()[0])
    test_message['error'] = str(sys.exc_info()[1]).strip()
    errors.exc(test_message)

# TODO Ensure I use a consistent name everywhere. Should be errors, not err.
found = False
if len(errors.log) > 0:
    for entry in errors.log:
        if len(entry) > 0:
            if entry[1] == 'exception':
                if 'message' in entry[2]:
                    if entry[2]['message'] == test_message:
                        found = True
                        break

assert found is True, "errors.exc()"
good("errors.exc()")