print("Starting test_temp_file")
import debugging
import temp_file
from uos import remove
from test_suite import good

tmp_dir = '/flash/tmp'
test_file = '/flash/testing.tst'
test_file_basename = test_file.split('/')[-1]

# FIXME Should also work if the file does not already exist
with open(test_file, 'w') as f:
    f.write('Testing')

my_temp = temp_file.create(test_file)
with open(my_temp, 'w') as f:
    f.write('Testing')

check = 'create()'
try:
    with open(tmp_dir + '/' + test_file_basename + '.tmp') as f:
        assert f.read() == 'Testing', check
except OSError:
    # FIXME [Errno 2] ENOENT
    raise AssertionError(check)

good(check)

remove(my_temp)

check = 'install()'
my_temp = temp_file.create(test_file)
with open(my_temp, 'w') as f:
    f.write('Testing')

temp_file.install(my_temp, test_file)

with open(test_file) as f:
    assert f.read() == 'Testing', check
good(check)