Deltacloud backend for Heat
===========================

`Heat(http://heat-api.org/)`_ brings orchestration, autoscaling and high availability to `OpenStack(http://www.openstack.org/)`_. Since January 2013, it's possible to configure Heat to use a backend other than OpenStack.

This project makes `Deltacloud(http://deltacloud.apache.org/)`_ into a backend Heat that can use. This means you can utilise Heat to provision your deployments on oVirt, EC2, Rackspace and `anything else that Deltacloud supports(http://deltacloud.apache.org/supported-providers.html)`_.

Prerequisities
--------------

* `Deltacloud server 1.1.0 or higher(http://deltacloud.apache.org/download.html)`_

* `Heat ``2013.1.g3`` or higher(https://github.com/openstack/heat/tags)`_
  (i.e. what's going to be the G release. You have to build it from source for now)


Setup
-----

#. Install the Deltacloud server and start it

#. Install Heat

#. ``pip install deltacloud_heat``

#. Add this line to `/etc/heat/heat-engine.conf`::

    cloud_backend=deltacloud_heat

#. Add the following lines to `/etc/heat/heat-api.conf`::

    [paste_deploy]
    flavor = custombackend

#. Start Heat engine, API and all the other services.


Authentication
--------------

Pass the username, password and Deltacloud entrypoint url via the `X-Auth-User`, `X-Auth-Key` and `X-Auth-URL` HTTP headers to the Heat API requests:

    curl -v -H 'accept: application/json' -H 'content-type: application/json' \
    -H 'x-auth-user: mockuser' -H 'x-auth-key: mockpassword' \
    -H 'x-auth-url: http://localhost:3002/api' \
    http://localhost:8004/v1/admin/stacks


Development status
------------------

Extremely early. Don't expect anything to work at this time. Bugs, comments, patches are very much welcome.


License
-------

Apache License, version 2.0