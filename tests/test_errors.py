from err import ErrCls
errors = ErrCls(debug = True, testing = True)
# FIXME Load the data_store and ensure the data got saved.
# TODO Also somehow need to determine if deepsleep() was called. Maybe a
# wrapper?

test_message = "Test message"

errors.warning(test_message)
assert test_message in errors.log, "errors.warn failed"
print("[SUCCESS] errors.warn")

# Clear the log
errors.log = list()

errors.err(test_message)
assert test_message in errors.log, "errors.err failed"
print("[SUCCESS] errors.err")

try:
    raise RuntimeError("Testing exception logging")
except RuntimeError:
    test_message = {'file': __file__, 'func': __name__,
                    'action': "Testing exception logging"}
    errors.exc(test_message)
    
assert test_message in errors.log, "errors.exc failed"
print("[SUCCESS] errors.exc")

errors.log = list()