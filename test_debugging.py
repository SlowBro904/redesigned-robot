import debugging
from test_suite import good

debug = debugging.printmsg

check = "printmsg()"
assert debug("Test") == print("[DEBUG] Test"), check
good(check)