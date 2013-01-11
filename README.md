Deltacloud client as a pluggable backend for Heat.

# Setup

1. Install OpenStack Heat with the pluggable-clients patches in:

   <https://github.com/tomassedovic/heat/tree/pluggable-clients>

   (the patches should be merged to the upstream soon)

2. Install Deltacloud version 1.0.5

3. Instal the latest Deltacloud client for Python

   <https://github.com/tomassedovic/deltacloud/tree/python-client/clients/python>

   (will get this merged into upstream soon and plan to put it to pypy, too)

4. Make the `deltacloud_heat` package importable by Heat Engine

   E.g. by manually putting it into your global or user `site-packages`, modifying your `sitecustomize.py`, making a proper setup.py and installing it that way.

   (proper `setup.py` will happen, same for pypy availability.)

5. Update Heat config to use the Deltacloud backend:

  5.1. Put `cloud_backend=deltacloud_heat.clients` to `/etc/heat/heat-engine.conf`

  5.2. Put the following into `/etc/heat/heat-api.conf`

        [paste_deploy]
        flavor = custombackend

6. Start Heat engine, API and all the other services.


# Authentication

Pass the username, password and Deltacloud entrypoint url via the `X-Auth-User`, `X-Auth-Key` and `X-Auth-URL` HTTP headers to the Heat API requests:

    curl -v -H 'accept: application/json' -H 'content-type: application/json' \
    -H 'x-auth-user: mockuser' -H 'x-auth-key: mockpassword' \
    -H 'x-auth-url: http://localhost:3002/api' \
    http://localhost:8004/v1/admin/stacks


# Development status

Extremely early. Don't expect anything to work at this time. Bugs, comments, patches are very much welcome.


# License

Apache License, version 2.0