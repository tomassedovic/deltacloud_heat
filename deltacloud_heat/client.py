'''
Deltacloud client that can be plugged into OpenStack Heat.
'''

import deltacloud

from deltacloud_heat.nova import NovaClient


class Clients(object):

    def __init__(self, context):
        self.context = context
        self.deltacloud_client = deltacloud.Deltacloud(self.context.auth_url,
            self.context.username, self.context.password)

    def keystone(self):
        pass

    def nova(self, service_type='compute'):
        return NovaClient(self.deltacloud_client)

    def swift(self):
        pass

    def quantum(self):
        pass

    def authenticated(self):
        return self.deltacloud_client.valid_credentials()
