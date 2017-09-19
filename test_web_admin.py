print("Starting test_web_admin")
import web_admin
from config import config
from test_suite import good

check = 'get_params()'
url = '/test?test=test'
assert web_admin.get_params(url) == ('/test', {'test': 'test'}), check
good(check)

check = 'get_template()'
# TODO This is kinda silly. Same code as in the function.
template = list()
with open(config.conf['WEB_ADMIN_TEMPLATE_FILE']) as f:
    for row in f.read():
        template.append(row)
template = '\n'.join(template)
assert template == web_admin.get_template(), check
good(check)

check = 'status()'
# Just making sure it returns True or False
assert isinstance(web_admin.status(), bool), check
good(check)