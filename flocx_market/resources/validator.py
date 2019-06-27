from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client


# Authenticate with the service user, and create a keystone client
auth = v3.Password(auth_url='https://127.0.0.1:5000/v3',
                   username='marketplace',
                   password='password',
                   project_name='admin',
                   user_domain_id='default',
                   project_domain_id='default')
sess = session.Session(auth=auth)
keystone = client.Client(session=sess)

# Validator-class that can easily be extended with functions
# that test role/project-access. self.validate contains a hash
# with information about this.
class Validator:
    def __init__(self, token):
        keystone.users.list()
        self.validate = keystone.tokens.validate(token)