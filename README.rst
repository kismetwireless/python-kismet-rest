kismet_rest
===========

Python wrapper for Kismet REST interface.

.. image:: https://readthedocs.org/projects/kismet-rest/badge/?version=latest
  :target: https://kismet-rest.readthedocs.io/en/latest/?badge=latest
  :alt: Documentation Status


Installing from PyPI
----------------------

::

    pip install kismet_rest


Installing from source
----------------------

::

    git clone https://github.com/kismetwireless/python-kismet-rest
    cd python-kismet-rest && pip install .


Usage examples
--------------

Authentication and setup
~~~~~~~~~~~~~~~~~~~~~~~~

Kismet now supports API tokens and roles. Use an API key with the ``admin`` role for controlling datasources, or a ``readonly`` key for queries. Pass it as ``apikey`` when creating an interface (basic auth via ``username`` / ``password`` also works).

Quickstart (modern API + API key):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    from kismet_rest import Datasources, Devices

    # Replace with your Kismet host and an API key (admin role for control)
    ds = Datasources(host_uri="http://127.0.0.1:2501", apikey="YOUR_ADMIN_API_KEY")

    # List datasources
    for src in ds.all():
        print(src["kismet.datasource.uuid"], src["kismet.datasource.name"])

    # Ensure a datasource is running (required before devices will appear)
    target_uuid = "<UUID_FROM_LIST>"
    ds.open(target_uuid)      # start it if it was not auto-started
    ds.set_hop(target_uuid)   # optional: enable hopping

    # Fetch recently active devices
    dev = Devices(host_uri="http://127.0.0.1:2501", apikey="YOUR_READONLY_OR_ADMIN_KEY")
    for device in dev.all(ts=0, fields=["kismet.device.base.macaddr"]):
        print(device.get("kismet.device.base.macaddr"))

Notes and troubleshooting
~~~~~~~~~~~~~~~~~~~~~~~~~

- Datasource control endpoints (pause/resume/close/open) require POST and the admin role in current Kismet releases.
- If no devices are returned, make sure at least one datasource is open/running; either configure it to auto-start in ``kismet.conf`` or call ``open(uuid)`` via the API.
- Device listing supports field simplification and regex filters; use the ``fields`` and ``regex`` kwargs with ``Devices.all`` to reduce response size.
- Tested against Kismet 2025-09-R1.

Legacy functionality (KismetConnector):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


::

    import kismet_rest
    conn = kismet_rest.KismetConnector(username="my_user", password="my_pass")
    for device in conn.device_summary():
        pprint.pprint(device)


Alerts since 2019-01-01:
~~~~~~~~~~~~~~~~~~~~~~~~

::

    import kismet_rest
    alerts = kismet_rest.Alerts()
    for alert in alerts.all(ts_sec=1546300800):
        print(alert)


Devices last observed since 2019-01-01:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    import kismet_rest
    devices = kismet_rest.Devices()
    for device in devices.all(ts=1546300800):
        print(device)


Developer notes:
----------------

* Formatting commit messages:
  * Correctly-formatted commit messages will be organized in CHANGELOG.rst
  * Commit messages are formatted like this ``type: audience: message !tag``
  * Type is for the type of change (``new``, ``chg``)
  * Audience is for the audience of the commit note(``usr``,``test``,``doc``)
  * The message part is pretty self-explanatory.
  * The optional tag allows you to flag a commit for exclusion from CHANGELOG.rst.(``minor`` or ``wip``)
  * A commit message like this: ``new: usr: Made a new widget.`` will appear in CHANGELOG.rst, under the appropriate release, under the "New" section.
  * More info on message formatting: https://github.com/vaab/gitchangelog
* Updating CHANGELOG.rst:
  * Install gitchangelog: ``pip3 install gitchangelog``
  * Make sure that ``__version__`` is correct in ``kismet_rest/__init__.py``
  * Build the new changelog: ``gitchangelog > CHANGELOG.rst``
