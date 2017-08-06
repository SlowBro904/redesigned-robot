import sys
import debugging
import test_suite
from err import ErrCls

def find_msg(msg_type, test_msg):
    '''Search for exactly our type and message in errors.log'''
    found = False
    if len(errors.log) > 0:
        for entry in errors.log:
            if len(entry) > 0:
                if entry[1] == msg_type:
                    if 'message' in entry[2]:
                        if entry[2]['message'] == test_msg:
                            return True

errors = ErrCls()

# TODO Somehow need to determine if deepsleep() was called. Maybe a wrapper?

good = test_suite.good

test_msg = "Test message"

errors.warn(test_msg)
assert find_msg('warning', test_msg) is True, "errors.warn()"
good("errors.warn()")

errors.err(test_msg)
assert find_msg('error', test_msg) is True, "errors.warn()"
good("errors.err()")

try:
    raise RuntimeError("errors.exc()")
except RuntimeError:
    test_msg = {'file': __file__, 'func': __name__,
                    'action': "Testing exception logging"}
    test_msg['exc_type'] = str(sys.exc_info()[0])
    test_msg['error'] = str(sys.exc_info()[1]).strip()
    errors.exc(test_msg)

# TODO Ensure I use a consistent name everywhere. Should be errors, not err.
assert find_msg('exception', test_msg) is True, "errors.warn()"
good("errors.exc()")