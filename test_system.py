from test_suite import good
from system import SystemCls
print("Starting test_system")

system = SystemCls()
assert len(system.version.split('.')) == 3, "system.version"
good("system.version")
assert len(system.attached_devices) >= 2, "system.attached_devices"
good("system.attached_devices")
assert 'door_reed_switches' in system.attached_devices, "door in devices"
good("door in devices")