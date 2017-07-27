from cloud import cloud
assert cloud.ping() is True, "cloud.ping() failed"
print("[SUCCESS] cloud.ping() succeeded"

assert cloud.can_login() is True, "cloud.can_login() failed"
print("[SUCCESS] cloud.can_login() succeeded"

assert cloud.encryption_working() is True, "cloud.encryption_working() failed"
print("[SUCCESS] cloud.encryption_working() succeeded"

assert cloud.isconnected() is True, "cloud.isconnected() failed"
print("[SUCCESS] cloud.isconnected() succeeded"