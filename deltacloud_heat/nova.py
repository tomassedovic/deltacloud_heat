'''
A Nova client for the Heat Deltacloud backend.

It uses an API compatible with the `novaclient`.
'''
from datetime import datetime
from random import randint
from novaclient.exceptions import NotFound


class KeyPair(object):
    def __init__(self, name):
        self.name = name


class ListWrapper(object):
    def __init__(self, items):
        self.items = items

    def list(self):
        return self.items


class Instance(object):
    def __init__(self, dc_instance):
        self.dc_instance = dc_instance

    @property
    def id(self):
        return self.dc_instance.id

    @property
    def name(self):
        return self.dc_instance.name

    @property
    def status(self):
        mapping = {
            'START': 'BUILD',
            'PENDING': 'BUILD',
            'RUNNING': 'ACTIVE',
            'UNKNOWN': 'UNKNOWN',
            'STOPPED': 'DELETED',
            'FINISH': 'DELETED',
        }
        return mapping[self.dc_instance.state]

    @property
    def networks(self):
        return {'private': self.dc_instance.private_addresses}

    def get(self):
        try:
            self.dc_instance.refresh()
        except:
            raise NotFound(404)

    def add_floating_ip(self, ip_address):
        pass

    def remove_floating_ip(self, ip_address):
        pass

    def delete(self):
        self.dc_instance.stop()
        self.dc_instance.destroy()


class FloatingIP(object):
    def __init__(self):
        self.id = 'floating-ip-%d' % randint(1, 100)
        self.ip = '127.0.0.1'

class Volume(object):
    def __init__(self, dc_volume):
        self.dc_volume = dc_volume

    def get(self):
        try:
            self.dc_volume.refresh()
        except:
            raise NotFound(404)

    @property
    def status(self):
        mapping = {
            'AVAILABLE': 'available',
            'IN-USE': 'in-use',
            'CREATING': 'creating',
            'STOPPED': 'deleted',
            'FINISH': 'deleted',
        }
        return mapping[self.dc_volume.state]

    @property
    def id(self):
        return self.dc_volume.id


class VolumeAttachment(object):
    def __init__(self, dc_client, dc_volume, dc_instance):
        self.dc_volume = dc_volume
        self.dc_instance = dc_instance
        self.dc_client = dc_client

    @property
    def id(self):
        return self.dc_volume.id


class SecurityGroup(object):
    def __init__(self, name):
        self.id = 'security-group-%d' % randint(1, 100)
        self.name = name
        self.rules = [{'id': 'mock_rule'}, {'id': 'mock_rule_2'}]


class ServersHandler(object):
    def __init__(self, deltacloud):
        self.client = deltacloud

    def create(self, *args, **kwargs):
        opts = {}
        opts['name'] = kwargs['name']
        opts['hwp_id'] = kwargs['flavor']
        opts['image_id'] = kwargs['image']
        opts['keyname'] = kwargs['key_name']

        # So we should be checking here to see if user-data is supported by looking
        # at the 'features' part of the dcloud api.
        opts['user_data'] = kwargs['userdata']

        # Still to set:
        # security groups

        dc_instance = self.client.create_instance(kwargs['image'], opts)
        return Instance(dc_instance)

    def get(self, instance_id):
        try:
            return Instance(self.client.instances(id=instance_id))
        except:
            raise NotFound(404)


class FloatingIPsHandler(object):
    def create(self):
        return FloatingIP()

    def get(self, instance_id):
        raise NotFound(404)

    def delete(self, instance_id):
        pass


class VolumesHandler(object):
    def __init__(self, deltacloud):
        self.client = deltacloud
        self.volume_id = -1

    #
    #    vol = self.nova('volume').volumes.create(self.properties['Size'],
    #                        display_name=self.physical_resource_name(),
    #                        display_description=self.physical_resource_name())

    def create(self, *args, **kwargs):
        opts = {}
        opts['capacity'] = args[0]
        opts['name'] = kwargs['display_name']
        print "Creating storage volume: %s" % opts
        dc_volume = self.client.create_storage_volume(opts)
        self.volume_id = dc_volume.id
        self.dc_volume = dc_volume
        return Volume(dc_volume)

    def create_server_volume(self, *args, **kwargs):
        server_id = kwargs['server_id']
        self.volume_id = kwargs['volume_id']
        device = kwargs['device']

        self.dc_volume = self.client.storage_volumes(id=self.volume_id)
        instance = self.client.instances(server_id)
        self.dc_volume.attach(instance, device)

        volume_attachment = VolumeAttachment(self.client, self.dc_volume, instance)
        return volume_attachment

    def get(self, id=None):
        try:
            if id is None:
                return Volume(self.client.storage_volumes(id=self.volume_id))
            else:
                return Volume(self.client.storage_volumes(id=id))
        except:
            raise NotFound(404)

    # Unattach..
    def delete_server_volume(self, server_id, volume_id):
        self.dc_volume = self.client.storage_volumes(id=volume_id)
        # DC Doesn't need instance to detach from..
        #instance = self.client.instances(server_id)
        self.dc_volume.detach()

    def delete(self):
        self.dc_volume.delete()


class VolumeAttachmentsHandler(object):
    def __init__(self, volumes_handler):
        self._attachments = []
        self._volumes_handler = volumes_handler

    def create_server_volume(self, *args, **kwargs):
        volume_attachment = VolumeAttachment(**kwargs)
        self._attachments.append(volume_attachment)
        self._volumes_handler.get(volume_attachment.id).status = 'in-use'
        return volume_attachment

    def delete_server_volume(self, server_id, volume_id):
        self._volumes_handler.get(volume_id).status = 'available'


class SecurityGroupsHandler(object):
    def __init__(self):
        self._groups = []

    def list(self):
        return self._groups

    def create(self, name, properties):
        group = SecurityGroup(name)
        self._groups.append(group)
        return group

    def get(self, id):
        found = [g for g in self._groups if g.id == id]
        if found:
            return found[0]
        raise NotFound(404)

    def delete(self, id):
        try:
            group = self.get(id)
            self._groups.remove(group)
        except:
            pass


class SecurityGroupRulesHandler(object):
    def create(self, *args, **kwargs):
        pass

    def delete(self, id):
        pass


FLOATING_IPS = FloatingIPsHandler()
SECURITY_GROUPS = SecurityGroupsHandler()
SECURITY_GROUP_RULES = SecurityGroupRulesHandler()


class NovaClient(object):
    def __init__(self, deltacloud_client):
        self.client = deltacloud_client

    @property
    def keypairs(self):
        return ListWrapper(self.client.keys())

    @property
    def images(self):
        return ListWrapper(self.client.images())

    @property
    def flavors(self):
        return ListWrapper(self.client.hardware_profiles())

    @property
    def volumes(self):
        return VolumesHandler(self.client)

    @property
    def servers(self):
        return ServersHandler(self.client)

    @property
    def floating_ips(self):
        return FLOATING_IPS

    @property
    def security_groups(self):
        return SECURITY_GROUPS

    @property
    def security_group_rules(self):
        return SECURITY_GROUP_RULES
